# 🚀 Azure Deployment Guide

## Quick Deployment Options

### Option 1: Automated Script (Recommended)
```bash
./deploy_to_azure.sh
```

### Option 2: Manual Azure Portal Deployment

1. **Go to Azure Portal**: https://portal.azure.com
2. **Create App Service**:
   - Click "Create a resource" → "Web App"
   - Choose your subscription and create/select resource group
   - App name: `gps-image-api-[your-unique-id]`
   - Runtime: `Python 3.11`
   - Region: Choose closest to your users
   - Pricing: `Free F1` (for testing) or `Basic B1` (for production)

3. **Deploy Code**:
   - Go to your App Service → "Deployment Center"
   - Choose "Local Git" or "GitHub" (if your code is on GitHub)
   - Follow the deployment instructions

### Option 3: Azure CLI Manual Steps

```bash
# Install Azure CLI (macOS)
brew install azure-cli

# Login
az login

# Create resource group
az group create --name gps-image-api-rg --location "East US"

# Create app service plan
az appservice plan create \
  --name gps-image-api-plan \
  --resource-group gps-image-api-rg \
  --sku F1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group gps-image-api-rg \
  --plan gps-image-api-plan \
  --name gps-image-api-[timestamp] \
  --runtime "PYTHON|3.11" \
  --deployment-local-git

# Configure startup
az webapp config set \
  --resource-group gps-image-api-rg \
  --name gps-image-api-[timestamp] \
  --startup-file "bash startup.sh"
```

## 🔧 Configuration Settings

### Environment Variables to Set in Azure:
- `WORKERS`: `1` (for Free tier) or `2-4` (for higher tiers)
- `MAX_IMAGE_SIZE_MB`: `3`
- `LOG_LEVEL`: `INFO`
- `PORT`: (automatically set by Azure)

### Scaling Recommendations:
- **Free F1**: 1 worker, good for testing
- **Basic B1**: 2 workers, good for light production
- **Standard S1+**: 4+ workers, good for production

## 🧪 Testing Your Deployment

After deployment, test with:
```bash
# Health check
curl https://your-app-name.azurewebsites.net/health

# Generate image
curl -X POST "https://your-app-name.azurewebsites.net/generate-image?latitude=40.7128&longitude=-74.0060&scalar=1.5" \
  --output azure_test.jpg

# Or use the test script
python test_api.py https://your-app-name.azurewebsites.net
```

## 📊 Monitoring

1. **Application Insights**: Enable in Azure Portal for detailed monitoring
2. **Log Stream**: View real-time logs in Azure Portal
3. **Metrics**: Monitor CPU, memory, and request metrics

## 🔍 Troubleshooting

### Common Issues:

1. **App won't start**:
   - Check startup.sh has correct permissions
   - Verify Python version compatibility
   - Check Application Logs in Azure Portal

2. **Slow performance**:
   - Upgrade from Free F1 to Basic B1 or higher
   - Increase worker count
   - Enable Application Insights for performance monitoring

3. **Memory issues**:
   - Monitor memory usage in Azure Portal
   - Consider upgrading to higher tier
   - Optimize image generation code

4. **Timeout errors**:
   - Increase timeout in startup.sh
   - Optimize image generation performance
   - Consider async processing for large images

### Log Locations:
- **Application Logs**: Azure Portal → App Service → Log stream
- **Deployment Logs**: Azure Portal → App Service → Deployment Center
- **System Logs**: Available via Kudu console

## 🔄 Continuous Deployment

### GitHub Actions (Recommended):
1. Fork/push your code to GitHub
2. In Azure Portal → App Service → Deployment Center
3. Choose GitHub and authorize
4. Select your repository and branch
5. Azure will create a GitHub Actions workflow automatically

### Manual Updates:
```bash
# After making changes
git add .
git commit -m "Update API"
git push azure main
```

## 💰 Cost Optimization

- **Free F1**: $0/month (good for testing, has limitations)
- **Basic B1**: ~$13/month (good for light production)
- **Standard S1**: ~$56/month (production with auto-scaling)

## 🔐 Security Considerations

1. **Add authentication** if needed (Azure AD, API keys)
2. **Enable HTTPS only** (default in Azure)
3. **Set up CORS** if accessed from web browsers
4. **Monitor for abuse** with rate limiting
5. **Use Azure Key Vault** for sensitive configuration

## 📈 Performance Tips

1. **Enable caching** for frequently requested coordinates
2. **Use Azure CDN** for global distribution
3. **Implement async processing** for complex image generation
4. **Monitor and optimize** image generation algorithms
5. **Consider Azure Functions** for serverless scaling
