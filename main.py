from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel, Field, field_validator
import logging
import io
from PIL import Image
import numpy as np
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GPS Image Generator API",
    description="API that generates images based on GPS position and scalar value",
    version="1.0.0"
)

class GPSPosition(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    
    @field_validator('latitude')
    @classmethod
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90 degrees')
        return v

    @field_validator('longitude')
    @classmethod
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180 degrees')
        return v

class ImageRequest(BaseModel):
    gps_position: GPSPosition
    scalar: float = Field(..., description="Scalar value for image generation")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "GPS Image Generator API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check endpoint for Azure"""
    return {"status": "healthy", "service": "gps-image-api"}

@app.post("/generate-image")
async def generate_image(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude in decimal degrees"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude in decimal degrees"),
    scalar: float = Query(..., description="Scalar value for image generation")
):
    """
    Generate an image based on GPS position and scalar value.
    
    Args:
        latitude: GPS latitude (-90 to 90)
        longitude: GPS longitude (-180 to 180)
        scalar: Scalar value for image generation
    
    Returns:
        Image file (JPEG format, max 2-3MB)
    """
    try:
        logger.info(f"Generating image for GPS: ({latitude}, {longitude}), scalar: {scalar}")
        
        # Validate inputs
        gps_position = GPSPosition(latitude=latitude, longitude=longitude)
        
        # TODO: Replace this placeholder with actual image generation logic
        image = generate_placeholder_image(latitude, longitude, scalar)
        
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=85, optimize=True)
        img_byte_arr.seek(0)
        
        # Check image size (should be max 2-3MB)
        image_size = len(img_byte_arr.getvalue())
        logger.info(f"Generated image size: {image_size / (1024*1024):.2f} MB")
        
        if image_size > 3 * 1024 * 1024:  # 3MB limit
            logger.warning(f"Image size ({image_size / (1024*1024):.2f} MB) exceeds 3MB limit")
            # Could implement compression here if needed
        
        return Response(
            content=img_byte_arr.getvalue(),
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f"inline; filename=gps_image_{latitude}_{longitude}_{scalar}.jpg",
                "Content-Length": str(image_size)
            }
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

def generate_placeholder_image(latitude: float, longitude: float, scalar: float) -> Image.Image:
    """
    Placeholder function for image generation.
    This will be replaced with your actual image generation logic.
    """
    # Create a simple placeholder image
    width, height = 800, 600
    
    # Create a gradient based on GPS coordinates and scalar
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Use GPS coordinates to influence colors
    red_intensity = int(((latitude + 90) / 180) * 255)
    green_intensity = int(((longitude + 180) / 360) * 255)
    blue_intensity = int((scalar % 1) * 255)
    
    # Create a simple pattern
    for y in range(height):
        for x in range(width):
            img_array[y, x] = [
                (red_intensity + x // 4) % 256,
                (green_intensity + y // 4) % 256,
                (blue_intensity + (x + y) // 8) % 256
            ]
    
    return Image.fromarray(img_array)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
