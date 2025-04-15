"""Deployment script for ContentFlow AI.

This script deploys the ContentFlow AI platform to Modal Labs.
"""

import os
import sys
import argparse
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the deployment configurations
from modal.deployment import stub
from src.models.serving.vllm_service import vllm_stub


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
    
    # Deploy the specified service(s)
    if service == "all" or service == "main":
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
    
    deploy(environment=args.env, service=args.service)


if __name__ == "__main__":
    main()
