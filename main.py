from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response, HTMLResponse
from pydantic import BaseModel, Field, field_validator
import logging
import io
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from typing import Optional
import os
import random
import math
from dotenv import load_dotenv
import pygal
from pygal.style import Style
# import cairosvg  # Not needed for Railway deployment
from datetime import datetime
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom CSS for bigger, bold fonts and icons
custom_css = """
/* Make all fonts 20% bigger and bold */
body, .swagger-ui {
    font-size: 120% !important;
    font-weight: bold !important;
}

/* Headers bigger and bolder */
.swagger-ui h1, .swagger-ui h2, .swagger-ui h3, .swagger-ui h4, .swagger-ui h5, .swagger-ui h6 {
    font-size: 140% !important;
    font-weight: 900 !important;
}

/* API title */
.swagger-ui .info .title {
    font-size: 180% !important;
    font-weight: 900 !important;
}

/* Operation summaries */
.swagger-ui .opblock .opblock-summary {
    font-size: 130% !important;
    font-weight: bold !important;
}

/* Parameter names and descriptions */
.swagger-ui .parameter__name {
    font-size: 120% !important;
    font-weight: bold !important;
}

/* Buttons */
.swagger-ui .btn {
    font-size: 120% !important;
    font-weight: bold !important;
    padding: 12px 24px !important;
}

/* Method badges (GET, POST, etc.) */
.swagger-ui .opblock .opblock-summary-method {
    font-size: 120% !important;
    font-weight: 900 !important;
    min-width: 80px !important;
}

/* Response codes */
.swagger-ui .responses-inner h4 {
    font-size: 130% !important;
    font-weight: bold !important;
}

/* Input fields */
.swagger-ui input[type=text], .swagger-ui input[type=number], .swagger-ui textarea {
    font-size: 120% !important;
    font-weight: bold !important;
    padding: 12px !important;
}

/* Code blocks */
.swagger-ui .highlight-code {
    font-size: 115% !important;
    font-weight: bold !important;
}

/* Navigation and sections */
.swagger-ui .scheme-container {
    font-size: 120% !important;
    font-weight: bold !important;
}

/* Make expand/collapse icons bigger */
.swagger-ui .opblock-summary-control:focus svg, .swagger-ui .opblock-summary-control:hover svg {
    transform: scale(1.3) !important;
}

/* Response section styling */
.swagger-ui .response-col_description {
    font-size: 120% !important;
    font-weight: bold !important;
}

/* Parameter descriptions */
.swagger-ui .parameter__type {
    font-size: 115% !important;
    font-weight: bold !important;
}

/* Model names */
.swagger-ui .model-title {
    font-size: 130% !important;
    font-weight: bold !important;
}
"""

app = FastAPI(
    title="GPS Image Generator API",
    description="API that generates images based on GPS position and scalar value",
    version="1.0.0",
    docs_url=None,  # Disable default docs
    redoc_url=None  # Disable redoc
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

@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI with bigger, bold fonts and icons"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GPS Image Generator API - Documentation</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css" />
        <style>
        {custom_css}
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
        <script>
        SwaggerUIBundle({{
            url: '/openapi.json',
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.presets.standalone
            ],
            layout: "BaseLayout",
            deepLinking: true,
            showExtensions: true,
            showCommonExtensions: true
        }});
        </script>
    </body>
    </html>
    """

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
        image.save(img_byte_arr, format='PNG', optimize=True)
        img_byte_arr.seek(0)

        # Check image size (should be max 2-3MB)
        image_size = len(img_byte_arr.getvalue())
        logger.info(f"Generated image size: {image_size / (1024*1024):.2f} MB")

        if image_size > 3 * 1024 * 1024:  # 3MB limit
            logger.warning(f"Image size ({image_size / (1024*1024):.2f} MB) exceeds 3MB limit")
            # Could implement compression here if needed

        return Response(
            content=img_byte_arr.getvalue(),
            media_type="image/png",
            headers={
                "Content-Disposition": f"inline; filename=gps_image_{latitude}_{longitude}_{scalar}.png",
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
    Generate a 4:3 PNG image with GPS-based information and icons.
    """
    # 4:3 aspect ratio dimensions - larger for 2x4 layout
    width, height = 1600, 1200

    # Create base image with RGBA support for transparency
    image = Image.new('RGBA', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    # Load background if available
    try:
        # Get absolute path to be sure
        current_dir = os.getcwd()
        background_path = os.path.join(current_dir, 'AiLandIcons', 'background.jpg')
        logger.info(f"Current working directory: {current_dir}")
        logger.info(f"Looking for background at: {background_path}")
        logger.info(f"Background exists: {os.path.exists(background_path)}")

        if os.path.exists(background_path):
            logger.info("Loading background...")
            background = Image.open(background_path)
            logger.info(f"Background loaded, size: {background.size}, mode: {background.mode}")
            # Use full color background without overlay
            background_resized = background.resize((width, height), Image.Resampling.LANCZOS)
            background_resized = background_resized.convert('RGBA')
            image.paste(background_resized, (0, 0))
            logger.info("Full color background pasted successfully")
        else:
            logger.warning(f"Background not found at {background_path}")
            # Create a gradient background as fallback
            logger.info("Creating fallback gradient background")
            for y in range(height):
                color_intensity = int(255 * (1 - y / height * 0.3))
                draw.rectangle([0, y, width, y+1], fill=(color_intensity, color_intensity, 255))
    except Exception as e:
        logger.error(f"Could not load background: {e}")
        # Create a gradient background as fallback
        logger.info("Creating fallback gradient background due to error")
        for y in range(height):
            color_intensity = int(255 * (1 - y / height * 0.3))
            draw.rectangle([0, y, width, y+1], fill=(color_intensity, color_intensity, 255))

    # Generate GPS-based data
    gps_data = generate_gps_data(latitude, longitude, scalar)

    # Draw the information panels
    draw_information_panels(image, gps_data, latitude, longitude)

    # Convert back to RGB for PNG output
    return image.convert('RGB')

def generate_gps_data(latitude: float, longitude: float, scalar: float) -> dict:
    """
    Generate realistic GPS-based environmental data.
    In a real implementation, this would call actual APIs or databases.
    """
    # Use GPS coordinates and scalar to generate realistic-looking data
    random.seed(int((latitude * 1000 + longitude * 1000 + scalar * 100) % 1000))

    # Height above sea level (in meters) - random 0-300
    height = random.randint(0, 300)

    # Fire risk - random 0-5%
    fire_risk = random.randint(0, 5)

    # Landslide risk - random 0-5%
    landslide_risk = random.randint(0, 5)

    # Slope calculation - random 0-100 degrees
    slope = random.randint(0, 100)

    # Weather data
    temperature = round(random.uniform(20, 42), 1)  # 20-42°C
    rain_probability = random.randint(0, 100)  # 0-100%

    # Wind speed - random 0-25 knots
    wind_speed = random.randint(0, 25)

    return {
        'gps_position': f"{latitude:.4f}, {longitude:.4f}",
        'fire_risk': fire_risk,
        'height': height,
        'landslide_risk': landslide_risk,
        'slope': slope,
        'temperature': temperature,
        'rain_probability': rain_probability,
        'wind_speed': wind_speed
    }

def draw_information_panels(image: Image.Image, data: dict, latitude: float, longitude: float):
    """
    Draw information panels with icons and data on the image.
    """
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Try to load regular fonts with multiple fallbacks and larger sizes
    def get_font(size):
        # Regular font paths - explicitly try lighter fonts first
        font_paths = [
            "/System/Library/Fonts/HelveticaNeue.ttc",  # macOS - Helvetica Neue (lighter)
            "/System/Library/Fonts/Helvetica.ttc",  # macOS - try Helvetica (lighter)
            "/System/Library/Fonts/Times.ttc",  # macOS - Times (lighter)
            "/System/Library/Fonts/Arial.ttf",  # macOS - Arial as fallback
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",  # Linux
            "/usr/share/fonts/TTF/arial.ttf",  # Some Linux
            "arial.ttf",  # Windows
            "Arial.ttf",  # Windows
        ]

        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, size)
                logger.info(f"Successfully loaded font: {font_path} at size {size}")
                return font
            except Exception as e:
                logger.debug(f"Failed to load font {font_path}: {e}")
                continue

        # If no TrueType font found, use default font but log it
        logger.warning(f"No TrueType fonts found, using default font at size {size}")
        try:
            return ImageFont.load_default()
        except:
            return None

    # Moderately bigger fonts to avoid bold appearance
    title_font = get_font(24)      # Moderately increased
    content_font = get_font(36)    # Moderately increased
    desc_font = get_font(16)       # Moderately increased
    small_font = get_font(12)      # Moderately increased



    # Date in top right corner
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    if title_font:
        date_bbox = draw.textbbox((0, 0), current_date, font=title_font)
        date_width = date_bbox[2] - date_bbox[0]
        draw.text((width - date_width - 20, 20), current_date, fill='white', font=title_font)
    else:
        # Fallback without bold effect
        draw.text((width - 200, 20), current_date, fill='white')

    # Define panel layout (2 columns, 4 rows) - 8 modules total
    panel_width = (width - 160) // 2  # Wider panels
    panel_height = 250  # Much taller for proper charts
    start_y = 80   # Start from top (below date)
    margin = 50  # Modules closer together

    # Generate chart data
    import random
    random.seed(int(latitude * longitude * 1000))  # Consistent data based on location

    # Fire risk over year (0-5%)
    fire_months = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    fire_data = [random.uniform(0, 5) for _ in range(12)]

    # Landslide risk over year (0-5%)
    landslide_data = [random.uniform(0, 5) for _ in range(12)]

    # Weather forecast for next week
    week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    wind_forecast = [random.uniform(0, 25) for _ in range(7)]  # 0-25 knots
    temp_forecast = [random.uniform(20, 42) for _ in range(7)]  # 20-42°C
    rain_forecast = [random.uniform(0, 100) for _ in range(7)]  # 0-100%

    panels = [
        {'icon': 'gps.png', 'title': 'GPS Position', 'content': data['gps_position'], 'desc': 'Coordinates of the location', 'chart_type': 'none'},
        {'icon': 'fire.jpg', 'title': 'Fire Risk', 'content': f"{data['fire_risk']}%", 'desc': 'Fire risk percentage', 'chart_type': 'yearly', 'chart_data': fire_data, 'chart_labels': fire_months},
        {'icon': 'height.jpg', 'title': 'Elevation', 'content': f"{data['height']}m", 'desc': 'Height above sea level', 'chart_type': 'none'},
        {'icon': 'landslides.jpg', 'title': 'Landslide Risk', 'content': f"{data['landslide_risk']}%", 'desc': 'Landslide risk percentage', 'chart_type': 'yearly', 'chart_data': landslide_data, 'chart_labels': fire_months},
        {'icon': 'slope.png', 'title': 'Slope', 'content': f"{data['slope']}°", 'desc': 'Terrain slope in degrees', 'chart_type': 'none'},
        {'icon': 'wind.jpg', 'title': 'Wind Speed', 'content': f"{data['wind_speed']} knots", 'desc': 'Wind speed in knots', 'chart_type': 'wind_forecast', 'chart_data': wind_forecast, 'chart_labels': week_days},
        {'icon': 'temperature.png', 'title': 'Temperature', 'content': f"{data['temperature']}°C", 'desc': 'Current temperature', 'chart_type': 'temp_forecast', 'chart_data': temp_forecast, 'chart_labels': week_days},
        {'icon': 'weather.jpg', 'title': 'Rain Forecast', 'content': f"{data['rain_probability']}%", 'desc': 'Rain probability', 'chart_type': 'rain_forecast', 'chart_data': rain_forecast, 'chart_labels': week_days},
    ]

    def get_windfinder_color(value, chart_type):
        """Get Windfinder-style colors based on value and chart type"""
        if chart_type == 'wind_forecast':
            # Wind speed colors (0-25 knots): Green -> Yellow -> Orange -> Red
            if value <= 5: return '#00FF00'       # Bright green (light wind)
            elif value <= 10: return '#7FFF00'   # Yellow-green
            elif value <= 15: return '#FFFF00'   # Yellow
            elif value <= 20: return '#FFA500'   # Orange
            else: return '#FF0000'               # Red (strong wind)

        elif chart_type == 'temp_forecast':
            # Temperature colors (20-42°C): Blue -> Green -> Yellow -> Orange -> Red
            if value <= 25: return '#0080FF'     # Blue (cool)
            elif value <= 30: return '#00FF80'   # Green-blue
            elif value <= 35: return '#00FF00'   # Green (comfortable)
            elif value <= 38: return '#FFFF00'   # Yellow (warm)
            elif value <= 40: return '#FFA500'   # Orange (hot)
            else: return '#FF0000'               # Red (very hot)

        return '#3182CE'  # Default blue

    def create_fallback_chart(chart_type, chart_data, chart_labels, chart_width, chart_height):
        """Create a simple fallback chart using PIL when cairosvg is not available"""
        # Create a simple colored rectangle as fallback
        chart_image = Image.new('RGB', (chart_width, chart_height), 'white')
        draw = ImageDraw.Draw(chart_image)

        # Draw a simple bar chart representation
        if chart_data:
            max_val = max(chart_data) if chart_data else 1
            bar_width = chart_width // len(chart_data) if chart_data else chart_width

            for i, value in enumerate(chart_data):
                if max_val > 0:
                    bar_height = int((value / max_val) * (chart_height - 40))
                    x1 = i * bar_width + 10
                    y1 = chart_height - bar_height - 20
                    x2 = x1 + bar_width - 5
                    y2 = chart_height - 20

                    # Use different colors based on chart type
                    if 'fire' in chart_type.lower():
                        color = '#FF6B6B'
                    elif 'landslide' in chart_type.lower():
                        color = '#8A2BE2'
                    elif 'wind' in chart_type.lower():
                        color = '#4ECDC4'
                    elif 'temp' in chart_type.lower():
                        color = '#45B7D1'
                    else:
                        color = '#2563EB'

                    draw.rectangle([x1, y1, x2, y2], fill=color, outline='gray')

        # Add title if provided with MUCH bigger font
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)   # MUCH bigger - doubled from 8
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
            except:
                font = ImageFont.load_default()

        draw.text((10, 5), f"Chart: {chart_type}", fill='black', font=font)

        return chart_image

    def create_pygal_chart(chart_type, chart_data, chart_labels, chart_width, chart_height, is_landslide=False, chart_title=""):
        """Create beautiful Pygal charts with Windfinder-style colors"""

        # Beautiful style
        beautiful_style = Style(
            background='white',
            plot_background='white',
            foreground='#333',
            foreground_strong='#333',
            foreground_subtle='#999',
            opacity='1.0',
            opacity_hover='0.8',
            transition='150ms ease-in',
            colors=('#E53E3E', '#38A169', '#3182CE', '#805AD5', '#D69E2E')
        )

        # Violet style for landslide
        violet_style = Style(
            background='white',
            plot_background='white',
            foreground='#333',
            foreground_strong='#333',
            foreground_subtle='#999',
            opacity='1.0',
            opacity_hover='0.8',
            transition='150ms ease-in',
            colors=('#8A2BE2',)  # Violet color
        )

        if chart_type == 'yearly':
            # Smooth filled area chart for yearly data
            chart_style = violet_style if is_landslide else beautiful_style
            chart = pygal.Line(
                style=chart_style,
                width=chart_width,
                height=chart_height,
                show_legend=False,
                show_dots=False,  # No dots for smooth curves
                fill=True,        # Fill the area under curve
                interpolate='cubic',  # Smooth curves
                interpolation_parameters={'type': 'kochanek_bartels', 'nb_points': 300},
                margin=20,
                x_label_rotation=0,
                show_minor_x_labels=True,   # Show x-axis values
                show_minor_y_labels=False,
                label_font_size=14,        # MUCH bigger - doubled from 7
                major_label_font_size=16,  # MUCH bigger - doubled from 7
                value_font_size=14,        # MUCH bigger - doubled from 7
                show_y_guides=True,
                show_x_guides=False,
                range=(0, 10),
                title=chart_title,  # Add chart title
                title_font_size=16         # MUCH bigger - doubled from 8
            )
            chart.x_labels = chart_labels
            chart.add('', chart_data, fill=True)

        elif chart_type in ['wind_forecast', 'temp_forecast']:
            # Windfinder-style colored bars - limit to 7 data points
            chart = pygal.Bar(
                style=beautiful_style,
                width=chart_width,
                height=chart_height,
                show_legend=False,
                margin=20,
                spacing=5,
                x_label_rotation=0,
                show_minor_x_labels=True,   # Show x-axis values
                show_minor_y_labels=False,
                label_font_size=14,        # MUCH bigger - doubled from 7
                major_label_font_size=16,  # MUCH bigger - doubled from 7
                value_font_size=14,        # MUCH bigger - doubled from 7
                show_y_guides=True,
                show_x_guides=False,
                range=(0, 25) if chart_type == 'wind_forecast' else (20, 42),
                title=chart_title,  # Add chart title
                title_font_size=16         # MUCH bigger - doubled from 8
            )
            # Limit to first 7 data points and labels
            chart.x_labels = chart_labels[:7]

            # Add all bars as one series with individual colors - limit to 7 values
            colored_data = []
            for value in chart_data[:7]:
                color = get_windfinder_color(value, chart_type)
                colored_data.append({'value': value, 'color': color})
            chart.add('', colored_data)

        elif chart_type == 'rain_forecast':
            # Blue line chart for rain - straight lines, no smoothing
            # Create custom blue style
            blue_style = Style(
                background='white',
                plot_background='white',
                foreground='#333',
                foreground_strong='#333',
                foreground_subtle='#666',
                colors=['#2563EB'],  # Force blue color
                stroke_width=2,
                stroke_dasharray='0'
            )

            chart = pygal.Line(
                style=blue_style,
                width=chart_width,
                height=chart_height,
                show_legend=False,
                show_dots=False,  # No dots - clean line
                fill=False,       # No fill under line
                interpolate=None,  # No smoothing - straight lines between points
                margin=20,
                x_label_rotation=0,
                show_minor_x_labels=True,   # Show x-axis values
                show_minor_y_labels=False,
                label_font_size=14,        # MUCH bigger - doubled from 7
                major_label_font_size=16,  # MUCH bigger - doubled from 7
                value_font_size=14,        # MUCH bigger - doubled from 7
                show_y_guides=True,
                show_x_guides=False,
                range=(0, 100),
                title=chart_title,  # Add chart title
                title_font_size=16         # MUCH bigger - doubled from 8
            )
            chart.x_labels = chart_labels[:7]  # Limit to 7 days
            chart.add('', chart_data[:7])  # Blue line

        # Try to render as PNG directly (if cairosvg is available)
        try:
            import cairosvg
            # Render chart to SVG
            svg_data = chart.render()
            # Convert SVG to PNG with high quality
            png_data = cairosvg.svg2png(
                bytestring=svg_data,
                output_width=chart_width,
                output_height=chart_height,
                dpi=150  # High DPI for crisp rendering
            )
            # Convert to PIL Image
            chart_image = Image.open(BytesIO(png_data))
        except (ImportError, OSError):
            # Fallback: create a simple chart using PIL
            logger.warning("cairosvg not available, using fallback chart rendering")
            chart_image = create_fallback_chart(chart_type, chart_data, chart_labels, chart_width, chart_height)

        return chart_image

    logger.info(f"Drawing {len(panels)} panels in 2x4 layout")
    for i, panel in enumerate(panels):
        # Calculate position (2 columns, 4 rows to fit 8 panels)
        col = i % 2
        row = i // 2
        x = margin + col * (panel_width + margin)
        y = start_y + row * (panel_height + 25)  # Closer spacing between rows


        # Use full panel width for 2 columns
        actual_panel_width = panel_width

        # Draw panel background (white with slight transparency)
        # Create a transparent overlay for the panel (90% opacity = 10% transparency)
        panel_overlay = Image.new('RGBA', (actual_panel_width, panel_height), (255, 255, 255, 230))
        image.paste(panel_overlay, (x, y), panel_overlay)

        # Draw panel border
        draw.rectangle([x, y, x + actual_panel_width, y + panel_height],
                      fill=None, outline='gray', width=2)

        # Draw icon (increased by 20% more, total 92% increase)
        icon_size = int(48 * 1.92)  # 92% increase = 92.16 ≈ 92 pixels
        icon_x = x + 10
        icon_y = y + 10

        try:
            current_dir = os.getcwd()
            icon_path = os.path.join(current_dir, 'AiLandIcons', panel['icon'])
            if os.path.exists(icon_path):
                icon = Image.open(icon_path)
                icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                if icon.mode == 'RGBA':
                    image.paste(icon, (icon_x, icon_y), icon)
                else:
                    image.paste(icon, (icon_x, icon_y))
        except Exception as e:
            # Draw placeholder
            draw.rectangle([icon_x, icon_y, icon_x + icon_size, icon_y + icon_size],
                         fill='lightgray', outline='gray', width=2)

        # Draw text content
        text_x = icon_x + icon_size + 10
        text_width = actual_panel_width - icon_size - 30

        # Title (no bold effect)
        if title_font:
            draw.text((text_x, y + 10), panel['title'], fill='black', font=title_font)
        else:
            # Fallback: simple text
            draw.text((text_x, y + 10), panel['title'], fill='black')

        # Content (larger font, no bold effect)
        if content_font:
            draw.text((text_x, y + 50), panel['content'], fill='darkblue', font=content_font)
        else:
            # Fallback: simple text
            draw.text((text_x, y + 50), panel['content'], fill='darkblue')

        # Draw chart if applicable - BEAUTIFUL PYGAL CHARTS
        if panel.get('chart_type') != 'none' and panel.get('chart_type'):
            chart_x = x + 10
            chart_y = y + 111  # Move charts up by 9 pixels total (4 more)
            chart_width = actual_panel_width - 20
            chart_height = int(110 * 1.25)  # Increase height by 25%

            # Create beautiful Pygal chart
            is_landslide = 'Landslide' in panel['title']

            # Determine chart title based on chart type
            chart_title = ""
            if panel['chart_type'] == 'yearly':
                if 'Fire' in panel['title']:
                    chart_title = "annual risk"
                elif 'Landslide' in panel['title']:
                    chart_title = "annual risk"
            elif panel['chart_type'] in ['wind_forecast', 'temp_forecast', 'rain_forecast']:
                chart_title = "week forecast"

            chart_image = create_pygal_chart(panel['chart_type'], panel['chart_data'], panel['chart_labels'],
                                           chart_width, chart_height, is_landslide, chart_title)

            # Resize chart if needed and paste it
            if chart_image.size != (chart_width, chart_height):
                chart_image = chart_image.resize((chart_width, chart_height), Image.Resampling.LANCZOS)

            # Paste the chart onto the main image
            image.paste(chart_image, (chart_x, chart_y))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
