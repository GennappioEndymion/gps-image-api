import requests
import json
import os
from PIL import Image
import io

def test_api_locally():
    """Test the API running locally"""
    base_url = "http://localhost:8000"
    
    print("Testing GPS Image Generator API...")
    
    # Test health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test image generation
    print("\n2. Testing image generation...")
    test_cases = [
        {"latitude": 40.7128, "longitude": -74.0060, "scalar": 1.5},  # New York
        {"latitude": 51.5074, "longitude": -0.1278, "scalar": 2.0},   # London
        {"latitude": 35.6762, "longitude": 139.6503, "scalar": 0.5},  # Tokyo
    ]
    
    for i, params in enumerate(test_cases):
        print(f"\nTest case {i+1}: {params}")
        try:
            response = requests.post(
                f"{base_url}/generate-image",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                # Save the image
                filename = f"test_image_{i+1}.jpg"
                with open(filename, "wb") as f:
                    f.write(response.content)
                
                # Check image properties
                image = Image.open(io.BytesIO(response.content))
                size_mb = len(response.content) / (1024 * 1024)
                
                print(f"✅ Success! Image saved as {filename}")
                print(f"   Size: {size_mb:.2f} MB")
                print(f"   Dimensions: {image.size}")
                print(f"   Format: {image.format}")
                
            else:
                print(f"❌ Failed with status {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    # Test invalid inputs
    print("\n3. Testing input validation...")
    invalid_cases = [
        {"latitude": 91, "longitude": 0, "scalar": 1},      # Invalid latitude
        {"latitude": 0, "longitude": 181, "scalar": 1},     # Invalid longitude
        {"latitude": "invalid", "longitude": 0, "scalar": 1}, # Invalid type
    ]
    
    for i, params in enumerate(invalid_cases):
        print(f"\nInvalid test case {i+1}: {params}")
        try:
            response = requests.post(
                f"{base_url}/generate-image",
                params=params,
                timeout=10
            )
            
            if response.status_code == 400:
                print(f"✅ Correctly rejected with status {response.status_code}")
                error_detail = response.json().get("detail", "No detail")
                print(f"   Error message: {error_detail}")
            else:
                print(f"❌ Unexpected status {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")

def test_api_azure(azure_url):
    """Test the API deployed on Azure"""
    print(f"Testing API deployed at: {azure_url}")
    
    # Test health check
    try:
        response = requests.get(f"{azure_url}/health", timeout=10)
        print(f"Health check status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test image generation
    print("\nTesting image generation on Azure...")
    params = {"latitude": 40.7128, "longitude": -74.0060, "scalar": 1.5}
    
    try:
        response = requests.post(
            f"{azure_url}/generate-image",
            params=params,
            timeout=60  # Longer timeout for Azure
        )
        
        if response.status_code == 200:
            filename = "azure_test_image.jpg"
            with open(filename, "wb") as f:
                f.write(response.content)
            
            size_mb = len(response.content) / (1024 * 1024)
            print(f"✅ Success! Image saved as {filename}")
            print(f"   Size: {size_mb:.2f} MB")
            
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Test Azure deployment
        azure_url = sys.argv[1]
        test_api_azure(azure_url)
    else:
        # Test local deployment
        test_api_locally()
        
        print("\n" + "="*50)
        print("To test Azure deployment, run:")
        print("python test_api.py https://your-app-name.azurewebsites.net")
