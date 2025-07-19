# 🌍 GPS Image Generator API

Generate beautiful GPS information panels with environmental data, charts, and professional styling.

## 🚀 One-Click Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/YOUR-USERNAME/gps-image-api)

## 📡 API Usage

### Health Check
```bash
GET /health
```

### Generate GPS Image
```bash
POST /generate-image?latitude={lat}&longitude={lng}&scalar={scalar}
```

**Parameters:**
- `latitude`: Float (-90 to 90) - GPS latitude
- `longitude`: Float (-180 to 180) - GPS longitude  
- `scalar`: Float (0.1 to 10.0) - Data variation scaling

**Example:**
```bash
curl -X POST "https://your-api-url/generate-image?latitude=45.4642&longitude=9.1900&scalar=2.5" \
     --output gps_image.png
```

## 🎨 Generated Features

- **8 Information Panels**: GPS, Fire Risk, Elevation, Landslide, Slope, Wind, Temperature, Rain
- **Professional Charts**: Annual trends and 7-day forecasts
- **Beautiful Design**: Semi-transparent panels over full-color background
- **High Quality**: 1600x1200 PNG images

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Test
curl http://localhost:8000/health
```

## 📊 Example Locations

```bash
# Milan, Italy
curl -X POST "YOUR-API-URL/generate-image?latitude=45.4642&longitude=9.1900&scalar=2.5"

# New York, USA
curl -X POST "YOUR-API-URL/generate-image?latitude=40.7128&longitude=-74.0060&scalar=1.8"

# Tokyo, Japan
curl -X POST "YOUR-API-URL/generate-image?latitude=35.6762&longitude=139.6503&scalar=3.2"
```

## 🔧 Tech Stack

- **FastAPI** - Modern Python web framework
- **Pillow** - Image processing
- **Pygal** - Beautiful chart generation
- **Railway** - Cloud deployment
