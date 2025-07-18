# GPS Image Generator API

A FastAPI-based service that generates images based on GPS coordinates and scalar values, designed for deployment on Azure App Service.

## Features

- **GPS Input Validation**: Accepts latitude (-90 to 90) and longitude (-180 to 180) coordinates
- **Scalar Parameter**: Additional scalar value for image generation customization
- **Image Output**: Returns JPEG images (max 2-3MB) optimized for web delivery
- **Azure Ready**: Configured for Azure App Service deployment
- **Health Checks**: Built-in health check endpoints for monitoring
- **Error Handling**: Comprehensive error handling and logging

## API Endpoints

### `GET /`
Health check endpoint returning service status.

### `GET /health`
Azure-compatible health check endpoint.

### `POST /generate-image`
Main endpoint for image generation.

**Parameters:**
- `latitude` (float): GPS latitude in decimal degrees (-90 to 90)
- `longitude` (float): GPS longitude in decimal degrees (-180 to 180)  
- `scalar` (float): Scalar value for image generation

**Response:**
- Content-Type: `image/jpeg`
- Max size: 3MB
- Filename: `gps_image_{lat}_{lon}_{scalar}.jpg`

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```
   
   Or with uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - OpenAPI schema: http://localhost:8000/openapi.json

## Azure Deployment

### Option 1: Azure App Service (Recommended)

1. **Create Azure App Service:**
   ```bash
   az webapp create \
     --resource-group your-resource-group \
     --plan your-app-service-plan \
     --name your-app-name \
     --runtime "PYTHON|3.11" \
     --deployment-local-git
   ```

2. **Configure startup command:**
   ```bash
   az webapp config set \
     --resource-group your-resource-group \
     --name your-app-name \
     --startup-file "bash startup.sh"
   ```

3. **Deploy code:**
   ```bash
   git remote add azure https://your-app-name.scm.azurewebsites.net/your-app-name.git
   git push azure main
   ```

### Option 2: Azure DevOps Pipeline

1. Update `azure-pipelines.yml` with your service connection and app name
2. Create a new pipeline in Azure DevOps pointing to this repository
3. Run the pipeline to build and deploy

## Environment Variables

- `PORT`: Port number (default: 8000)
- `AZURE_STORAGE_CONNECTION_STRING`: Azure Storage connection string (optional)
- `AZURE_STORAGE_CONTAINER_NAME`: Storage container name (optional)
- `MAX_IMAGE_SIZE_MB`: Maximum image size in MB (default: 3)
- `LOG_LEVEL`: Logging level (default: INFO)

## Testing

Test the API using curl:

```bash
# Health check
curl http://localhost:8000/health

# Generate image
curl -X POST "http://localhost:8000/generate-image?latitude=40.7128&longitude=-74.0060&scalar=1.5" \
  --output generated_image.jpg
```

## Image Generation

The current implementation includes a placeholder image generation function. Replace the `generate_placeholder_image()` function in `main.py` with your actual image generation logic.

## Production Considerations

- **Image Size**: Monitor generated image sizes to stay within the 3MB limit
- **Performance**: Consider implementing caching for frequently requested coordinates
- **Storage**: Optionally integrate with Azure Blob Storage for image persistence
- **Monitoring**: Use Azure Application Insights for monitoring and logging
- **Security**: Add authentication/authorization as needed
- **Rate Limiting**: Consider implementing rate limiting for production use
