Modal Labs FastAPI Service Setup Guide
Based on the latest Modal Labs API documentation from 2025, here's a complete guide to set up an HTTP call and FastAPI service with Modal Labs.
Step 1: Install Modal
First, you need to install Modal and set up your account:
bashpip install modal
modal token new
This will prompt you to create an account if you don't have one already and set up your API token.
Step 2: Choose Your Implementation
I've created three artifacts for you:

Basic Modal FastAPI Service - A simple API with GET and POST endpoints
API Client - Python code to call your Modal API endpoints
Advanced Modal API - Shows more features like GPU acceleration, authentication, and shared data

Step 3: Deploy Your Service

Save the code from the "Modal FastAPI Service" artifact to a file named app.py
Deploy it to Modal Labs:

bashmodal deploy app.py
After deployment, Modal will give you URLs for your endpoints, which will look something like:

https://yourworkspace--data-service-get-data.modal.run
https://yourworkspace--data-service-submit-data.modal.run

The URLs follow the pattern: https://<source>--<label>.modal.run where <source> is your workspace name and <label> is the function name or custom label you specified. Modal + 2
Step 4: Use Your API Client

Save the code from the "API Client" artifact to a file named client.py
Update the URLs in the script with your actual Modal endpoint URLs
Run the client:

bashpython client.py
Step 5: Advanced Features (Optional)
If you want to use the advanced features:

Save the code from the "Advanced Modal API" artifact to a file named advanced_api.py
Create a secret for authentication:

bashmodal secret create api-auth-token AUTH_TOKEN=your-secure-token-here

Deploy the advanced API:

bashmodal deploy advanced_api.py
Key Features Demonstrated

Basic GET/POST Endpoints: Using @modal.fastapi_endpoint() decorator to easily create API endpoints Modal
Streaming Responses: The advanced API shows how you can use FastAPI's StreamingResponse for real-time data Modal
Data Processing: Shows how to connect API endpoints to background processing functions and handle job queues Ehsan's BlogModal
Authentication: Using Bearer tokens with FastAPI security dependencies Modal
Documentation: Setting docs=True enables interactive OpenAPI documentation at /docs endpoint Modal

Making HTTP Calls to Your API
You can call your API using any HTTP client - here are some examples:
Using curl:
bash# GET request
curl "https://yourworkspace--data-service-get-data.modal.run?query=electronics"

# POST request
curl -X POST "https://yourworkspace--data-service-submit-data.modal.run" \
     -H "Content-Type: application/json" \
     -d '{"name":"Product D","category":"Books","price":19.99}'
Using Python requests (as shown in the client):
pythonimport requests

# GET request
response = requests.get(
    "https://yourworkspace--data-service-get-data.modal.run",
    params={"query": "electronics"}
)
print(response.json())

# POST request
response = requests.post(
    "https://yourworkspace--data-service-submit-data.modal.run",
    json={"name": "Product D", "category": "Books", "price": 19.99}
)
print(response.json())
Notes and Best Practices

The fastapi_endpoint decorator supports customization through parameters like method, label, docs, and requires_proxy_auth Modal
Use modal serve app.py during development for hot-reloading of local changes Modal
Keep your Modal token secure and never commit it to public repositories
For production applications, consider adding proper error handling and validation Modal
For web applications, you can combine Modal with frontend frameworks by mounting static files Modal