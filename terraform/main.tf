### main.tf ###
# This file contains all of the resources that will be deployed and managed by Terraform.

########## STORAGE ##########
resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.resource_group_location
  account_tier             = "Standard"
  account_replication_type = "GRS"
}

resource "azurerm_storage_container" "input_container" {
  name                 = "input"
  storage_account_name = azurerm_storage_account.storage.name
}

resource "azurerm_storage_container" "output_container" {
  name                 = "output"
  storage_account_name = azurerm_storage_account.storage.name
}

resource "azurerm_storage_queue" "input_queue" {
  name                 = "input"
  storage_account_name = azurerm_storage_account.storage.name
}

########## MONITOR ##########
resource "azurerm_log_analytics_workspace" "log_analytics" {
  name                = var.log_analytics_workspace_name
  resource_group_name = var.resource_group_name
  location            = var.resource_group_location
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_application_insights" "app_insights" {
  name                = var.application_insights_name
  resource_group_name = var.resource_group_name
  location            = var.resource_group_location
  application_type    = "web"
  workspace_id        = azurerm_log_analytics_workspace.log_analytics.id
  depends_on          = [azurerm_log_analytics_workspace.log_analytics]
}

########## COMPUTE ##########
resource "azurerm_service_plan" "service_plan" {
  name                = var.service_plan_name
  resource_group_name = var.resource_group_name
  location            = var.resource_group_location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "function" {
  name                       = var.function_app_name
  resource_group_name        = var.resource_group_name
  location                   = var.resource_group_location
  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key
  service_plan_id            = azurerm_service_plan.service_plan.id
  
  depends_on = [
    azurerm_storage_account.storage,
    azurerm_service_plan.service_plan,
    azurerm_application_insights.app_insights,
    azurerm_storage_container.input_container,
    azurerm_storage_container.output_container,
  ]

  site_config {
    always_on         = false
    ftps_state        = "AllAllowed"
    http2_enabled     = true
    use_32_bit_worker = false

    application_insights_connection_string = azurerm_application_insights.app_insights.connection_string

    application_stack {
      python_version = "3.8"
    }
  }

  identity {
    type = "SystemAssigned"
  }

  app_settings = {
    APP_INSIGHTS_CNX_STR               = azurerm_application_insights.app_insights.connection_string
    ENABLE_ORYX_BUILD                  = true
    PYTHON_ISOLATE_WORKER_DEPENDENCIES = 1
    STORAGE_ACCOUNT_NAME               = azurerm_storage_account.storage.name
    STORAGE_ACCOUNT_KEY                = azurerm_storage_account.storage.primary_access_key
    STORAGE_ACCOUNT_CNX_STR            = azurerm_storage_account.storage.primary_connection_string
    STORAGE_ACCOUNT_INPUT_CONTAINER    = azurerm_storage_container.input_container.name
    STORAGE_ACCOUNT_OUTPUT_CONTAINER   = azurerm_storage_container.output_container.name
  }

  lifecycle {
    ignore_changes = [app_settings["WEBSITE_RUN_FROM_PACKAGE"]]
  }
}

########## EVENTS ##########
resource "azurerm_eventgrid_event_subscription" "input_subscription" {
  name                 = var.event_grid_subscription_name
  scope                = azurerm_storage_account.storage.id
  included_event_types = ["Microsoft.Storage.BlobCreated"]

  storage_queue_endpoint {
    storage_account_id = azurerm_storage_account.storage.id
    queue_name         = azurerm_storage_queue.input_queue.name
  }

  subject_filter {
    subject_begins_with = "/blobServices/default/containers/${azurerm_storage_container.input_container.name}"
  }

  depends_on = [
    azurerm_linux_function_app.function,
    azurerm_storage_account.storage,
    azurerm_storage_container.input_container,
    azurerm_storage_queue.input_queue,
  ]
}
