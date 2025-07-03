#!/bin/bash

# Azure Setup Script for Fabric MCP Server
# This script helps set up the required Azure resources

set -e

echo "=== Azure Setup for Fabric MCP Server ==="
echo

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "Error: Azure CLI is not installed. Please install it first."
    echo "Visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Login to Azure
echo "Logging in to Azure..."
az login

# Get subscription
echo "\nSelect subscription:"
az account list --output table
read -p "Enter subscription ID: " SUBSCRIPTION_ID
az account set --subscription $SUBSCRIPTION_ID

# Set variables
read -p "Enter resource group name: " RESOURCE_GROUP
read -p "Enter location (e.g., westeurope): " LOCATION
read -p "Enter function app name: " FUNCTION_APP_NAME
read -p "Enter storage account name (lowercase, no spaces): " STORAGE_ACCOUNT

# Create resource group
echo "\nCreating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create storage account
echo "\nCreating storage account..."
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS

# Get storage key
STORAGE_KEY=$(az storage account keys list \
  --resource-group $RESOURCE_GROUP \
  --account-name $STORAGE_ACCOUNT \
  --query '[0].value' -o tsv)

# Create blob container for insights
echo "\nCreating blob container for insights..."
az storage container create \
  --name insights \
  --account-name $STORAGE_ACCOUNT \
  --account-key $STORAGE_KEY

# Create Application Insights
echo "\nCreating Application Insights..."
az monitor app-insights component create \
  --app $FUNCTION_APP_NAME-insights \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP

# Get Instrumentation Key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app $FUNCTION_APP_NAME-insights \
  --resource-group $RESOURCE_GROUP \
  --query instrumentationKey -o tsv)

# Create Function App
echo "\nCreating Function App..."
az functionapp create \
  --resource-group $RESOURCE_GROUP \
  --consumption-plan-location $LOCATION \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --name $FUNCTION_APP_NAME \
  --storage-account $STORAGE_ACCOUNT

# Configure Function App settings
echo "\nConfiguring Function App settings..."
az functionapp config appsettings set \
  --name $FUNCTION_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    "APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY" \
    "STORAGE_ACCOUNT_NAME=$STORAGE_ACCOUNT" \
    "STORAGE_ACCOUNT_KEY=$STORAGE_KEY"

# Create service principal for GitHub Actions
echo "\nCreating service principal for GitHub Actions..."
SP_NAME="$FUNCTION_APP_NAME-github-actions"
SP_OUTPUT=$(az ad sp create-for-rbac \
  --name $SP_NAME \
  --role contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP \
  --sdk-auth)

echo "\n=== Setup Complete ==="
echo
echo "Next steps:"
echo "1. Add these secrets to your GitHub repository:"
echo "   - AZURE_CREDENTIALS: (copy the JSON below)"
echo "$SP_OUTPUT"
echo
echo "2. Download publish profile from Azure Portal and add as:"
echo "   - AZURE_FUNCTIONAPP_PUBLISH_PROFILE"
echo
echo "3. Configure Fabric credentials in Function App settings"
echo
echo "Function App URL: https://$FUNCTION_APP_NAME.azurewebsites.net"
echo "Storage Account: $STORAGE_ACCOUNT"
echo "Application Insights: $FUNCTION_APP_NAME-insights"