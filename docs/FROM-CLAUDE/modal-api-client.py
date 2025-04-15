# client.py
import requests
import json

def call_get_endpoint(base_url, query=None):
    """
    Call the GET endpoint to retrieve data
    
    Args:
        base_url: The base URL of your Modal app (e.g., "https://yourworkspace--data-service-get-data.modal.run")
        query: Optional search parameter
        
    Returns:
        The JSON response from the API
    """
    url = base_url
    params = {}
    if query:
        params['query'] = query
    
    print(f"Making GET request to {url} with params {params}")
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Received status code {response.status_code}")
        return {"error": f"Request failed with status code {response.status_code}"}

def call_post_endpoint(base_url, data):
    """
    Call the POST endpoint to submit data
    
    Args:
        base_url: The base URL of your Modal app with the submit-data label
                 (e.g., "https://yourworkspace--data-service-submit-data.modal.run")
        data: Dictionary containing the data to submit
        
    Returns:
        The JSON response from the API
    """
    headers = {
        'Content-Type': 'application/json'
    }
    
    print(f"Making POST request to {base_url} with data {data}")
    response = requests.post(base_url, data=json.dumps(data), headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Received status code {response.status_code}")
        try:
            error_info = response.json()
            return {"error": f"Request failed: {error_info}"}
        except:
            return {"error": f"Request failed with status code {response.status_code}"}

if __name__ == "__main__":
    # Replace these URLs with your actual Modal endpoints
    get_data_url = "https://yourworkspace--data-service-get-data.modal.run"
    submit_data_url = "https://yourworkspace--data-service-submit-data.modal.run"
    
    # Example: Get all data
    print("\nGetting all data:")
    result = call_get_endpoint(get_data_url)
    print(json.dumps(result, indent=2))
    
    # Example: Get filtered data
    print("\nGetting filtered data:")
    result = call_get_endpoint(get_data_url, query="electronics")
    print(json.dumps(result, indent=2))
    
    # Example: Submit new data
    print("\nSubmitting new data:")
    new_data = {
        "name": "Product D",
        "category": "Books",
        "price": 19.99
    }
    result = call_post_endpoint(submit_data_url, new_data)
    print(json.dumps(result, indent=2))
