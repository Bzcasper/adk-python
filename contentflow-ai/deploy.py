"""Deployment script for ContentFlow AI.

This script deploys the ContentFlow AI platform to Modal Labs.
It handles environment setup and provides a simple CLI for deployment.
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime
import importlib.util

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = ["modal", "vllm", "torch", "fastapi", "pydantic"]
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Installing missing dependencies: {', '.join(missing_packages)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("Dependencies installed successfully.")


def deploy(environment="development", service="all"):
    """
    Deploy the ContentFlow AI platform to Modal Labs.
    
    Args:
        environment: The environment to deploy to (development, staging, production).
        service: The service to deploy (all, main, vllm).
    """
    print(f"Deploying ContentFlow AI to Modal Labs ({environment} environment, {service} service)...")
    
    # Set the environment variable for the deployment
    os.environ["MODAL_ENVIRONMENT"] = environment
    timestamp = datetime.now().strftime('%Y%m%d-%H%M')
    
    try:
        # Import the Modal stubs
        if service == "all" or service == "main":
            from modal.deployment import stub
            
            # Deploy the main ContentFlow AI app
            if environment == "production":
                # In production, we deploy the app with a specific label
                stub.deploy(
                    name="contentflow-ai",
                    label=f"prod-{timestamp}",
                )
            else:
                # In development, we deploy the app with a default label
                stub.deploy(
                    name="contentflow-ai-dev",
                    label=f"dev-{timestamp}",
                )
            print(f"ContentFlow AI main service deployed successfully to {environment} environment!")
        
        if service == "all" or service == "vllm":
            from src.models.serving.vllm_service import vllm_stub
            
            # Deploy the vLLM service
            if environment == "production":
                # In production, we deploy the app with a specific label
                vllm_stub.deploy(
                    name="contentflow-ai-vllm",
                    label=f"prod-{timestamp}",
                )
            else:
                # In development, we deploy the app with a default label
                vllm_stub.deploy(
                    name="contentflow-ai-vllm-dev",
                    label=f"dev-{timestamp}",
                )
            print(f"ContentFlow AI vLLM service deployed successfully to {environment} environment!")
        
        print(f"Deployment completed successfully!")
        
        # Print the URLs for the deployed services
        if service == "all" or service == "main":
            if environment == "production":
                print(f"Main API URL: https://contentflow-ai--prod.modal.run")
            else:
                print(f"Main API URL: https://contentflow-ai-dev--dev.modal.run")
        
        if service == "all" or service == "vllm":
            if environment == "production":
                print(f"vLLM API URL: https://contentflow-ai-vllm--prod.modal.run")
            else:
                print(f"vLLM API URL: https://contentflow-ai-vllm-dev--dev.modal.run")
        
    except Exception as e:
        print(f"Error during deployment: {str(e)}")
        print("Make sure you have the Modal CLI installed and configured correctly.")
        print("You can install it with: pip install modal")
        print("Then configure it with: modal token new")
        sys.exit(1)


def main():
    """Main entry point for the deployment script."""
    parser = argparse.ArgumentParser(description="Deploy ContentFlow AI to Modal Labs")
    parser.add_argument(
        "--env",
        choices=["development", "staging", "production"],
        default="development",
        help="Environment to deploy to (default: development)",
    )
    parser.add_argument(
        "--service",
        choices=["all", "main", "vllm"],
        default="all",
        help="Service to deploy (default: all)",
    )
    args = parser.parse_args()
    
    # Check dependencies
    check_dependencies()
    
    # Deploy the services
    deploy(environment=args.env, service=args.service)


if __name__ == "__main__":
    main()
