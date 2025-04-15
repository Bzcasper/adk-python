# advanced_api.py
import modal
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any, Optional
import time

# Create a more advanced image with additional dependencies
image = modal.Image.debian_slim().pip_install(
    "fastapi[standard]",
    "numpy",
    "pandas",
    "scikit-learn"
)

# Create a Modal app
app = modal.App("advanced-data-service")

# Create a shared dictionary to store data between function calls
shared_data = modal.Dict.new()

# Create a secret for API authentication
# In a real app, you would create this secret using the Modal CLI:
# modal secret create api-auth-token AUTH_TOKEN=your-secure-token-here
API_SECRET_NAME = "api-auth-token"  # Replace with your actual secret name

# Set up bearer token authentication
auth_scheme = HTTPBearer()

# Helper GPU function that simulates heavy computation
@app.function(gpu="any")
def process_with_gpu(data_id: str):
    """Simulate processing data with GPU acceleration"""
    # This would be your actual GPU-intensive code
    import numpy as np
    
    # Simulate processing time
    time.sleep(2)
    
    # Simulate result
    result = {
        "data_id": data_id,
        "status": "processed",
        "output": np.random.randn(5).tolist(),
        "processing_time": "2 seconds",
        "gpu_used": True
    }
    
    return result

# API endpoint with authentication
@app.function(
    image=image,
    secrets=[modal.Secret.from_name(API_SECRET_NAME, default={"AUTH_TOKEN": "default-dev-token"})]
)
@modal.fastapi_endpoint(docs=True)
async def secure_data(
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    """
    A secure endpoint that requires authentication
    """
    import os
    
    # Verify token
    if token.credentials != os.environ.get("AUTH_TOKEN", "default-dev-token"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Return secure data
    return {
        "message": "Authentication successful",
        "secure_data": [
            {"id": 101, "name": "Confidential Item A", "value": 9999},
            {"id": 102, "name": "Confidential Item B", "value": 8888}
        ]
    }

# Endpoint that uses GPU acceleration
@app.function(image=image)
@modal.fastapi_endpoint(method="POST")
async def process_data(data: Dict[str, Any]):
    """
    Process data using GPU acceleration via another Modal function
    
    Args:
        data: Dictionary with data to process, must include an 'id' field
        
    Returns:
        Processing results
    """
    if "id" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data must include an 'id' field"
        )
    
    # Store the original request in shared dictionary
    data_id = str(data["id"])
    shared_data[data_id] = data
    
    # Call the GPU function and wait for the result
    result = process_with_gpu.remote(data_id)
    
    # Return combined result
    return {
        "request": data,
        "result": result,
        "message": "Data processed successfully with GPU acceleration"
    }

# Endpoint to get all stored data
@app.function(image=image)
@modal.fastapi_endpoint()
def list_processed_data():
    """
    List all data that has been processed
    """
    # Convert the shared dictionary to a list
    data_list = [{"id": k, "data": v} for k, v in shared_data.items()]
    
    return {
        "count": len(data_list),
        "data": data_list
    }

# Main entrypoint for testing locally
@app.local_entrypoint()
def main():
    print("This script is meant to be deployed to Modal.")
    print("To deploy: modal deploy advanced_api.py")
    print("For local testing: modal serve advanced_api.py")

# To run this locally for development:
# modal serve advanced_api.py

# To deploy:
# modal deploy advanced_api.py
