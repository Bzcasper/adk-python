#!/usr/bin/env python
"""
Deployment script for ContentFlow AI API.

This script provides commands for deploying and testing the ContentFlow API
using Modal Labs.

Usage:
    python scripts/deploy_api.py [deploy|serve|token]
"""
import argparse
import os
import sys
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def deploy_api(env_name="dev"):
    """Deploy the API to Modal Labs."""
    print(f"Deploying ContentFlow API to Modal ({env_name} environment)...")
    
    # First activate the environment
    env_script = os.path.join(project_root, "scripts", "env_manager.py")
    result = subprocess.run(
        [sys.executable, env_script, "activate", env_name],
        check=False,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ Failed to activate environment")
        print(result.stderr)
        return False
    
    try:
        # Check if Modal is authenticated
        subprocess.run(["modal", "token"], check=True, capture_output=True)
        
        # Deploy the API
        result = subprocess.run(
            ["modal", "deploy", "src/api/deploy.py"],
            check=False,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Deployment complete!")
            print("\nAPI URL:")
            # Extract and display the URL from the output
            for line in result.stdout.splitlines():
                if "https://" in line and "modal.com" in line:
                    print(f"  {line.strip()}")
            return True
        else:
            print("❌ Deployment failed!")
            print("\nError details:")
            print(result.stderr)
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {str(e)}")
        print("\nPlease ensure you're logged in to Modal with 'modal token'")
        return False

def serve_locally(env_name="dev"):
    """Serve the API locally for testing."""
    print(f"Starting ContentFlow API locally ({env_name} environment)...")
    
    # First activate the environment
    env_script = os.path.join(project_root, "scripts", "env_manager.py")
    result = subprocess.run(
        [sys.executable, env_script, "activate", env_name],
        check=False,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ Failed to activate environment")
        print(result.stderr)
        return False
    
    try:
        subprocess.run(["modal", "serve", "src/api/deploy.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {str(e)}")
        print("\nPlease ensure Modal is properly installed and you're logged in.")
        return False

def generate_token():
    """Generate a JWT token for testing."""
    from jose import jwt
    import datetime
    
    # Get secret key from environment or use default
    secret_key = os.environ.get("CFLOW_JWT_SECRET", "dev-secret-key")
    
    # Create token payload
    payload = {
        "sub": "test-user",
        "role": "admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    
    # Generate token
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    print("\nTest JWT Token (valid for 24 hours):")
    print(f"{token}")
    print("\nUse in Authorization header as:")
    print(f"Bearer {token}")

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="ContentFlow API deployment tools")
    parser.add_argument("command", choices=["deploy", "serve", "token"],
                        help="Command to run (deploy, serve, or generate token)")
    parser.add_argument("--env", "-e", choices=["dev", "test", "prod"], default="dev",
                        help="Environment to use (default: dev)")
    
    args = parser.parse_args()
    
    if args.command == "deploy":
        deploy_api(args.env)
    elif args.command == "serve":
        serve_locally(args.env)
    elif args.command == "token":
        generate_token()

if __name__ == "__main__":
    main()
