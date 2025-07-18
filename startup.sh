#!/bin/bash

# Azure App Service startup script
echo "Starting GPS Image Generator API..."

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Start the application with Gunicorn
# Use fewer workers for basic tier, more for higher tiers
WORKERS=${WORKERS:-2}
gunicorn -w $WORKERS -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-8000} --timeout 120 --max-requests 1000 --max-requests-jitter 100
