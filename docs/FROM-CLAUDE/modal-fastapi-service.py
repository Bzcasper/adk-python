# app.py
import modal

# Create an image with FastAPI installed
image = modal.Image.debian_slim().pip_install("fastapi[standard]")

# Create a Modal app
app = modal.App("data-service")

# Define the FastAPI endpoint function
@app.function(image=image)
@modal.fastapi_endpoint(method="GET")
def get_data(query: str = None):
    """
    A simple API endpoint that returns data based on a query parameter.
    
    Args:
        query: Optional search term to filter data
        
    Returns:
        JSON response with data
    """
    # Sample data to return
    data = [
        {"id": 1, "name": "Product A", "category": "Electronics"},
        {"id": 2, "name": "Product B", "category": "Clothing"},
        {"id": 3, "name": "Product C", "category": "Food"},
    ]
    
    # Filter data if query parameter is provided
    if query:
        filtered_data = [item for item in data if query.lower() in item["name"].lower() 
                        or query.lower() in item["category"].lower()]
        return {"results": filtered_data, "query": query}
    
    return {"results": data}

# Create a POST endpoint to receive data
@app.function(image=image)
@modal.fastapi_endpoint(method="POST", label="submit-data")
def submit_data(item: dict):
    """
    An endpoint that accepts data via POST request
    
    Args:
        item: A dictionary with data to be processed
        
    Returns:
        JSON confirmation with the processed data
    """
    # Here you would typically store or process the data
    # For this example, we'll just return it with an ID
    if "id" not in item:
        item["id"] = 999  # Assign a dummy ID
    
    return {
        "status": "success",
        "message": "Data received",
        "data": item
    }

# To run this locally for development:
# modal serve app.py

# To deploy:
# modal deploy app.py
