### data.tf ###
# This file contains existing resources that will be used in our IaC.

# az environment variables
data "azurerm_client_config" "current" {}

# az subscription variables
data "azurerm_subscription" "current" {}
