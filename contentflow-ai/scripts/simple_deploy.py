#!/usr/bin/env python
"""
Simple Deployment Script for ContentFlow AI API.

This script provides simplified commands for deploying and testing the ContentFlow API
using Modal Labs, without Unicode characters or complex Modal CLI commands.

Usage:
    python scripts/simple_deploy.py [deploy|serve|token] [--env ENV]
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
    env_script = os.path.join(project_root, "scripts", "simple_env_manager.py")
    result = subprocess.run(
        [sys.executable, env_script, env_name],
        check=False,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("[ERROR] Failed to activate environment")
        print(result.stderr)
        return False
    
    try:
        # Deploy the API
        result = subprocess.run(
            ["modal", "deploy", "src/api/deploy.py"],
            check=False,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("[SUCCESS] Deployment complete!")
            print("\nAPI URL:")
            # Extract and display the URL from the output
            for line in result.stdout.splitlines():
                if "https://" in line and "modal.com" in line:
                    print(f"  {line.strip()}")
            return True
        else:
            print("[ERROR] Deployment failed!")
            print("\nError details:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        print("\nPlease ensure Modal is properly installed and configured")
        return False

def serve_locally(env_name="dev"):
    """Serve the API locally for testing."""
    print(f"Starting ContentFlow API locally ({env_name} environment)...")
    
    # First activate the environment
    env_script = os.path.join(project_root, "scripts", "simple_env_manager.py")
    result = subprocess.run(
        [sys.executable, env_script, env_name],
        check=False,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("[ERROR] Failed to activate environment")
        print(result.stderr)
        return False
    
    try:
        subprocess.run(["modal", "serve", "src/api/deploy.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {str(e)}")
        print("\nPlease ensure Modal is properly installed and configured")
        return False
    except KeyboardInterrupt:
        print("\n[INFO] Local server stopped")
        return True

def generate_token():
    """Generate a JWT token for testing."""
    try:
        # Try to import jwt, if not available use a fallback
        try:
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
        except ImportError:
            print("[ERROR] python-jose package not installed")
            print("\nTo install required package:")
            print("pip install python-jose[cryptography]")
            print("\nFallback token (for testing only):")
            print("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0LXVzZXIiLCJyb2xlIjoiYWRtaW4ifQ.TYZlFSUQ7U1vQcfbNxV9zI-TmKXPJXvZ2jGZJMTKLtU")
            print("\nUse in Authorization header as:")
            print("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0LXVzZXIiLCJyb2xlIjoiYWRtaW4ifQ.TYZlFSUQ7U1vQcfbNxV9zI-TmKXPJXvZ2jGZJMTKLtU")
    except Exception as e:
        print(f"[ERROR] Failed to generate token: {str(e)}")

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
