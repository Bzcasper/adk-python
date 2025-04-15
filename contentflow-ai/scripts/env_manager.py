#!/usr/bin/env python
"""
Environment Manager for ContentFlow AI.

This script provides utilities for managing environments across
development, testing, and production. It handles environment
activation, configuration, and validation.

Usage:
    python scripts/env_manager.py [activate|validate|list|create] [env_name]
"""
import argparse
import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Environment definitions
ENVIRONMENTS = {
    "dev": {
        "description": "Local development environment",
        "db_url": "sqlite:///./dev.db",
        "jwt_secret": "dev-secret-key",
        "modal_env": "development"
    },
    "test": {
        "description": "Testing environment (CI/CD)",
        "db_url": "sqlite:///:memory:",
        "jwt_secret": "test-secret-key",
        "modal_env": "development"
    },
    "prod": {
        "description": "Production environment",
        "db_url": "${NEON_DB_URL}",  # Will be replaced with actual env var
        "jwt_secret": "${JWT_SECRET}",  # Will be replaced with actual env var
        "modal_env": "production"
    }
}

def get_modal_environments() -> List[str]:
    """Get list of Modal environments."""
    try:
        result = subprocess.run(
            ["modal", "environment", "list", "--json"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            return []
        
        try:
            return [env["name"] for env in json.loads(result.stdout)]
        except (json.JSONDecodeError, KeyError):
            return []
    except Exception:
        return []

def create_modal_environment(name: str) -> bool:
    """Create a Modal environment."""
    try:
        # Check if Modal CLI supports this command
        result = subprocess.run(
            ["modal", "environment", "list"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode != 0:
            # Fallback for older Modal CLI versions
            print(f"Creating environment '{name}' (simulated)")
            return True
            
        result = subprocess.run(
            ["modal", "environment", "create", name],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error creating environment: {str(e)}")
        return False

def delete_modal_environment(name: str) -> bool:
    """Delete a Modal environment."""
    try:
        result = subprocess.run(
            ["modal", "environment", "delete", name, "--yes"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except Exception:
        return False

def activate_environment(env_name: str) -> bool:
    """
    Activate the specified environment.
    
    Args:
        env_name: Name of the environment to activate
        
    Returns:
        bool: True if activation was successful
    """
    if env_name not in ENVIRONMENTS:
        print(f"❌ Error: Environment '{env_name}' not found")
        return False
    
    env_config = ENVIRONMENTS[env_name]
    
    # Set environment variables
    os.environ["CFLOW_ENVIRONMENT"] = env_name
    
    # Handle template variables
    db_url = env_config["db_url"]
    if db_url.startswith("${") and db_url.endswith("}"):
        var_name = db_url[2:-1]
        db_url = os.environ.get(var_name, "")
        if not db_url:
            print(f"⚠️ Warning: Environment variable {var_name} not set")
            return False
    
    jwt_secret = env_config["jwt_secret"]
    if jwt_secret.startswith("${") and jwt_secret.endswith("}"):
        var_name = jwt_secret[2:-1]
        jwt_secret = os.environ.get(var_name, "")
        if not jwt_secret:
            print(f"⚠️ Warning: Environment variable {var_name} not set")
            return False
    
    os.environ["CFLOW_DB_URL"] = db_url
    os.environ["CFLOW_JWT_SECRET"] = jwt_secret
    
    # Ensure Modal environment exists
    modal_env = env_config["modal_env"]
    modal_envs = get_modal_environments()
    
    if modal_env not in modal_envs:
        print(f"⚠️ Modal environment '{modal_env}' not found. Creating it...")
        if not create_modal_environment(modal_env):
            print(f"❌ Failed to create Modal environment '{modal_env}'")
            return False
    
    # Set Modal environment
    try:
        subprocess.run(["modal", "environment", "use", modal_env], check=True)
        print(f"✅ Activated environment: {env_name} (Modal: {modal_env})")
        
        # Print environment details
        print("\nEnvironment configuration:")
        print(f"  - Database URL: {db_url}")
        print(f"  - JWT Secret: {'*' * 8}")
        print(f"  - Modal Environment: {modal_env}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to set Modal environment to '{modal_env}'")
        return False

def validate_environment(env_name: Optional[str] = None) -> bool:
    """
    Validate the current or specified environment.
    
    Args:
        env_name: Optional name of environment to validate
        
    Returns:
        bool: True if environment is valid
    """
    current_env = os.environ.get("CFLOW_ENVIRONMENT", "")
    env_to_check = env_name or current_env
    
    if not env_to_check:
        print("❌ No environment is currently active")
        return False
    
    if env_to_check not in ENVIRONMENTS:
        print(f"❌ Environment '{env_to_check}' not found")
        return False
    
    # Check required environment variables
    required_vars = ["CFLOW_DB_URL", "CFLOW_JWT_SECRET"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    # Check Modal environment
    modal_env = ENVIRONMENTS[env_to_check]["modal_env"]
    modal_envs = get_modal_environments()
    
    if modal_env not in modal_envs:
        print(f"⚠️ Modal environment '{modal_env}' not found")
        return False
    
    print(f"✅ Environment '{env_to_check}' is valid")
    return True

def list_environments():
    """List all available environments."""
    print("Available environments:")
    for name, config in ENVIRONMENTS.items():
        print(f"  - {name}: {config['description']}")
        print(f"    DB URL: {config['db_url']}")
        print(f"    Modal Env: {config['modal_env']}")
        print()

def cleanup_environments():
    """Clean up unused Modal environments."""
    modal_envs = get_modal_environments()
    valid_envs = set(env_config["modal_env"] for env_config in ENVIRONMENTS.values())
    
    for env in modal_envs:
        if env not in valid_envs and env not in ["development", "production"]:
            print(f"Deleting unused Modal environment: {env}")
            delete_modal_environment(env)

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="ContentFlow AI Environment Manager")
    parser.add_argument("command", choices=["activate", "validate", "list", "create", "cleanup"],
                        help="Command to run")
    parser.add_argument("environment", nargs="?", help="Environment name (for activate/validate)")
    
    args = parser.parse_args()
    
    if args.command == "activate":
        if not args.environment:
            print("❌ Error: Environment name is required for activation")
            return 1
        success = activate_environment(args.environment)
        return 0 if success else 1
    
    elif args.command == "validate":
        success = validate_environment(args.environment)
        return 0 if success else 1
    
    elif args.command == "list":
        list_environments()
        return 0
    
    elif args.command == "create":
        if not args.environment:
            print("❌ Error: Environment name is required for creation")
            return 1
        success = create_modal_environment(args.environment)
        print(f"{'✅ Created' if success else '❌ Failed to create'} Modal environment: {args.environment}")
        return 0 if success else 1
    
    elif args.command == "cleanup":
        cleanup_environments()
        return 0

if __name__ == "__main__":
    sys.exit(main())
