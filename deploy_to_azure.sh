#!/bin/bash

# Azure Deployment Script for GPS Image Generator API
# This script will help you deploy the API to Azure App Service

echo "🚀 Azure Deployment Script for GPS Image Generator API"
echo "======================================================"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Installing now..."
    
    # Install Azure CLI on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            echo "Installing Azure CLI via Homebrew..."
            brew install azure-cli
        else
            echo "Please install Homebrew first, then run: brew install azure-cli"
            exit 1
        fi
    else
        echo "Please install Azure CLI manually: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
        exit 1
    fi
fi

# Login to Azure
echo "🔐 Logging into Azure..."
az login

# Set variables (you can modify these)
RESOURCE_GROUP="gps-image-api-rg"
APP_SERVICE_PLAN="gps-image-api-plan"
WEB_APP_NAME="gps-image-api-$(date +%s)"  # Unique name with timestamp
LOCATION="East US"
RUNTIME="PYTHON|3.11"

echo "📝 Using the following configuration:"
echo "   Resource Group: $RESOURCE_GROUP"
echo "   App Service Plan: $APP_SERVICE_PLAN"
echo "   Web App Name: $WEB_APP_NAME"
echo "   Location: $LOCATION"
echo "   Runtime: $RUNTIME"
echo ""

# Create resource group
echo "🏗️  Creating resource group..."
az group create --name $RESOURCE_GROUP --location "$LOCATION"

# Create App Service plan (Free tier for testing)
echo "📋 Creating App Service plan..."
az appservice plan create \
    --name $APP_SERVICE_PLAN \
    --resource-group $RESOURCE_GROUP \
    --sku F1 \
    --is-linux

# Create web app
echo "🌐 Creating web app..."
az webapp create \
    --resource-group $RESOURCE_GROUP \
    --plan $APP_SERVICE_PLAN \
    --name $WEB_APP_NAME \
    --runtime "$RUNTIME" \
    --deployment-local-git

# Configure startup command
echo "⚙️  Configuring startup command..."
az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --startup-file "bash startup.sh"

# Set environment variables
echo "🔧 Setting environment variables..."
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --settings \
        WORKERS=1 \
        MAX_IMAGE_SIZE_MB=3 \
        LOG_LEVEL=INFO

# Get deployment credentials
echo "🔑 Getting deployment credentials..."
DEPLOYMENT_URL=$(az webapp deployment source config-local-git \
    --name $WEB_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query url \
    --output tsv)

echo "✅ Azure resources created successfully!"
echo ""
echo "🚀 To deploy your code:"
echo "   1. Add the Azure remote:"
echo "      git remote add azure $DEPLOYMENT_URL"
echo ""
echo "   2. Deploy your code:"
echo "      git add ."
echo "      git commit -m 'Deploy GPS Image API'"
echo "      git push azure main"
echo ""
echo "🌐 Your app will be available at:"
echo "   https://$WEB_APP_NAME.azurewebsites.net"
echo ""
echo "📊 Monitor your app:"
echo "   https://portal.azure.com"
echo ""
echo "🧪 Test your deployment:"
echo "   python test_api.py https://$WEB_APP_NAME.azurewebsites.net"
