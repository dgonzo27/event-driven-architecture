### variables.tf ###
# This file contains the variable definitions for our Terraform resources.

variable "resource_group_name" {
  description = "The name of the Azure resource group."
  type        = string
}

variable "resource_group_location" {
  description = "The location for resources deployed to the Azure resource group."
  type        = string
}

variable "service_principal_secret" {
  description = "The client secret for the Azure service principal."
  type        = string
  sensitive   = true
}

variable "storage_account_name" {
  description = "The name of the Azure storage account for this solution."
  type        = string
}

variable "log_analytics_workspace_name" {
  description = "The name of the Azure log analytics workspace for this solution."
  type        = string
}

variable "application_insights_name" {
  description = "The name of the Azure application insights instance for this solution."
  type        = string
}

variable "service_plan_name" {
  description = "The name of the Azure compute service plan for this solution."
  type        = string
}

variable "function_app_name" {
  description = "The name of the Azure function app for this solution."
  type        = string
}

variable "event_grid_subscription_name" {
  description = "The name of the Azure event grid subscription for this solution."
  type        = string
}
