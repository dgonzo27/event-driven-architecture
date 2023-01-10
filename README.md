# event-driven-architecture

[![python version](https://img.shields.io/badge/Python-v3.8-blue?logo=python&logoColor=yellow)](https://www.python.org/) [![CI_CD GitHub_Actions](https://img.shields.io/badge/GitHub-Actions-blue?logo=githubactions&logoColor=black)](https://github.com/features/actions) [![provider azure](https://img.shields.io/badge/Provider-Azure-blue?logo=microsoftazure&logoColor=0078D4)](https://azure.microsoft.com/en-us/) [![iac terraform](https://img.shields.io/badge/IaC-Terraform-blue?logo=terraform&logoColor=7B42BC)](https://www.terraform.io)

This repository contains the code and instructions for running an event-driven solution in Azure based on file uploads to Azure Storage.

It leverages the following technologies and services:

1. GitHub Actions
2. Terraform
3. Azure Storage (Containers and Queues)
4. Azure Event Grid
5. Azure Functions
6. Azure Log Analytics

## Getting Started

To get started with this solution, follow the [youtube video](https://youtu.be/QGMfWWF72sc) and refer back to the pre-requisites below.

Pre-Requisites:

1. Create a [Microsoft Azure](https://azure.microsoft.com/en-us/) account and subscription.

2. In your account, create an [app registration and service principal](https://learn.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals).

3. In your account, create a new resource group or use the default resource group.

3. Create the following repository secrets in GitHub:

    - TERRAFORM_STORAGE_ACCOUNT_NAME
    - SOLUTION_STORAGE_ACCOUNT_NAME
    - RESOURCE_GROUP_NAME
    - AZURE_SP_CREDENTIALS

4. Update the desired resource names in the `terraform/terraform.tfvars` file.

5. Update the desired resource name of the Azure Function in the `.github/workflows/function-deploy.yml` file.

## Service Principal Secret

The Azure Service Principal secret that you store in GitHub should match the format shown below:

```json
{
  "clientId": "3984723**********",
  "clientSecret": "s298Q~***********",
  "subscriptionId": "lyk390-a*********",
  "tenantId": "na892bs*************"
}
```