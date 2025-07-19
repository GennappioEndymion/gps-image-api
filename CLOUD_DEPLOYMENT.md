# 🚀 Deploy GPS Image API to Cloud (Free Options)

Since Azure has quota limitations, here are **FREE** cloud deployment options that work immediately:

## 🚂 Option 1: Railway (Recommended - Easiest)

### Step 1: Setup
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Connect your GitHub account and select this repository

### Step 2: Configure
- Railway will auto-detect Python and use `railway.json`
- It will automatically install dependencies from `requirements.txt`
- Your app will be live in ~2-3 minutes

### Step 3: Get Your URL
- Railway will provide a URL like: `https://your-app-name.up.railway.app`
- **Your API will be available immediately!**

---

## 🎨 Option 2: Render (Also Free)

### Step 1: Setup
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repo

### Step 2: Configure
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`
- **Plan**: Free
- Uses `render.yaml` for configuration

### Step 3: Deploy
- Render will build and deploy automatically
- URL will be: `https://your-app-name.onrender.com`

---

## 🟣 Option 3: Heroku (Classic Choice)

### Step 1: Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Login
heroku login
```

### Step 2: Create and Deploy
```bash
# Create Heroku app
heroku create your-gps-api-name

# Deploy
git add .
git commit -m "Deploy GPS Image API"
git push heroku main
```

### Step 3: Access
- URL: `https://your-gps-api-name.herokuapp.com`

---

## 🐳 Option 4: Docker + Cloud Run (Google Cloud)

### Step 1: Build Docker Image
```bash
docker build -t gps-image-api .
docker tag gps-image-api gcr.io/YOUR-PROJECT-ID/gps-image-api
```

### Step 2: Deploy to Cloud Run
```bash
gcloud run deploy gps-image-api \
  --image gcr.io/YOUR-PROJECT-ID/gps-image-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 📡 Once Deployed - How to Call Your API

### Replace `YOUR-DEPLOYED-URL` with your actual URL:

**Railway**: `https://your-app-name.up.railway.app`
**Render**: `https://your-app-name.onrender.com`  
**Heroku**: `https://your-app-name.herokuapp.com`

### 🔍 Health Check
```bash
curl https://YOUR-DEPLOYED-URL/health
```

### 🖼️ Generate GPS Images
```bash
# Milan, Italy
curl -X POST "https://YOUR-DEPLOYED-URL/generate-image?latitude=45.4642&longitude=9.1900&scalar=2.5" \
     --output milan_gps.png

# New York, USA
curl -X POST "https://YOUR-DEPLOYED-URL/generate-image?latitude=40.7128&longitude=-74.0060&scalar=1.8" \
     --output nyc_gps.png

# London, UK
curl -X POST "https://YOUR-DEPLOYED-URL/generate-image?latitude=51.5074&longitude=-0.1278&scalar=1.5" \
     --output london_gps.png

# Tokyo, Japan
curl -X POST "https://YOUR-DEPLOYED-URL/generate-image?latitude=35.6762&longitude=139.6503&scalar=3.2" \
     --output tokyo_gps.png
```

### 🐍 Python Usage
```python
import requests

# Replace with your deployed URL
BASE_URL = "https://YOUR-DEPLOYED-URL"

# Test health
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Generate GPS image
params = {
    "latitude": 45.4642,   # Milan coordinates
    "longitude": 9.1900,
    "scalar": 2.5
}

response = requests.post(f"{BASE_URL}/generate-image", params=params)

if response.status_code == 200:
    with open("gps_image.png", "wb") as f:
        f.write(response.content)
    print("✅ GPS image saved as gps_image.png")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
```

### 🌐 JavaScript/Web Usage
```javascript
const BASE_URL = 'https://YOUR-DEPLOYED-URL';

async function generateGPSImage(lat, lng, scalar) {
    const params = new URLSearchParams({
        latitude: lat,
        longitude: lng,
        scalar: scalar
    });
    
    try {
        const response = await fetch(`${BASE_URL}/generate-image?${params}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            
            // Create download link
            const a = document.createElement('a');
            a.href = url;
            a.download = `gps_${lat}_${lng}.png`;
            a.click();
            
            return url;
        } else {
            console.error('Error:', response.status);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

// Usage examples
generateGPSImage(45.4642, 9.1900, 2.5);  // Milan
generateGPSImage(40.7128, -74.0060, 1.8); // NYC
```

---

## 🎯 Recommended: Railway Deployment

**Railway is the easiest and fastest option:**

1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **New Project** → Deploy from GitHub repo
4. **Select** your repository
5. **Wait 2-3 minutes** for deployment
6. **Get your URL** and start using the API!

**Your GPS Image API will be live on the internet in under 5 minutes!** 🚀

---

## 📊 What Your API Generates

Each call to `/generate-image` creates a beautiful 1600x1200 PNG with:

- **8 Information Panels**: GPS, Fire Risk, Elevation, Landslide Risk, Slope, Wind, Temperature, Rain
- **Professional Charts**: Annual risk trends and 7-day forecasts
- **Beautiful Design**: Semi-transparent panels over full-color background
- **Real Data**: Based on GPS coordinates and scaling factor

**Ready to deploy? Choose Railway for the fastest setup!** ⚡
