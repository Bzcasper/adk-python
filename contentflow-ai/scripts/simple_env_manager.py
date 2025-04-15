#!/usr/bin/env python
"""
Simple Environment Manager for ContentFlow AI.

This script provides basic utilities for managing environments across
development, testing, and production without Unicode characters or
complex Modal CLI commands.

Usage:
    python scripts/simple_env_manager.py [dev|test|prod]
"""
import os
import sys
import subprocess
from pathlib import Path

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

def activate_environment(env_name):
    """
    Activate the specified environment.
    
    Args:
        env_name: Name of the environment to activate
        
    Returns:
        bool: True if activation was successful
    """
    if env_name not in ENVIRONMENTS:
        print(f"[ERROR] Environment '{env_name}' not found")
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
            print(f"[WARNING] Environment variable {var_name} not set")
            db_url = "sqlite:///./fallback.db"
            print(f"[INFO] Using fallback database: {db_url}")
    
    jwt_secret = env_config["jwt_secret"]
    if jwt_secret.startswith("${") and jwt_secret.endswith("}"):
        var_name = jwt_secret[2:-1]
        jwt_secret = os.environ.get(var_name, "")
        if not jwt_secret:
            print(f"[WARNING] Environment variable {var_name} not set")
            jwt_secret = "fallback-secret-key"
            print(f"[INFO] Using fallback JWT secret")
    
    os.environ["CFLOW_DB_URL"] = db_url
    os.environ["CFLOW_JWT_SECRET"] = jwt_secret
    
    # Set Modal environment variable directly
    modal_env = env_config["modal_env"]
    os.environ["MODAL_ENVIRONMENT"] = modal_env
    
    print(f"[SUCCESS] Activated environment: {env_name}")
    print("\nEnvironment configuration:")
    print(f"  - Database URL: {db_url}")
    print(f"  - JWT Secret: {'*' * 8}")
    print(f"  - Modal Environment: {modal_env}")
    return True

def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/simple_env_manager.py [dev|test|prod]")
        print("\nAvailable environments:")
        for name, config in ENVIRONMENTS.items():
            print(f"  - {name}: {config['description']}")
        return 1
    
    env_name = sys.argv[1]
    success = activate_environment(env_name)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
