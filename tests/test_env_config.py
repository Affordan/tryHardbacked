#!/usr/bin/env python3
"""
Test script to verify environment variable configuration for Dify API keys.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def test_env_variables():
    """Test that all required environment variables are loaded correctly."""
    
    print("🔍 Testing Environment Variable Configuration")
    print("=" * 50)
    
    # Test variables
    variables = {
        "DIFY_API_URL": os.getenv("DIFY_API_URL"),
        "DIFY_API_KEY": os.getenv("DIFY_API_KEY"),
        "DIFY_WORKFLOW_API_URL": os.getenv("DIFY_WORKFLOW_API_URL"),
        "DIFY_QNA_WORKFLOW_API_KEY": os.getenv("DIFY_QNA_WORKFLOW_API_KEY"),
        "DIFY_MONOLOGUE_WORKFLOW_API_KEY": os.getenv("DIFY_MONOLOGUE_WORKFLOW_API_KEY"),
    }
    
    all_good = True
    
    for var_name, var_value in variables.items():
        if var_value:
            # Mask API keys for security
            if "API_KEY" in var_name and var_value:
                masked_value = var_value[:8] + "..." + var_value[-4:] if len(var_value) > 12 else "***"
                print(f"✅ {var_name}: {masked_value}")
            else:
                print(f"✅ {var_name}: {var_value}")
        else:
            print(f"❌ {var_name}: NOT SET")
            all_good = False
    
    print("=" * 50)
    
    if all_good:
        print("🎉 All environment variables are configured correctly!")
    else:
        print("⚠️  Some environment variables are missing. Please check your .env file.")
    
    return all_good

def test_config_import():
    """Test that config.py can import the variables correctly."""
    
    print("\n🔍 Testing Config Module Import")
    print("=" * 50)
    
    try:
        from app.core.config import (
            DIFY_API_URL, DIFY_API_KEY,
            DIFY_WORKFLOW_API_URL,
            DIFY_QNA_WORKFLOW_API_KEY,
            DIFY_MONOLOGUE_WORKFLOW_API_KEY
        )
        
        config_vars = {
            "DIFY_API_URL": DIFY_API_URL,
            "DIFY_API_KEY": DIFY_API_KEY,
            "DIFY_WORKFLOW_API_URL": DIFY_WORKFLOW_API_URL,
            "DIFY_QNA_WORKFLOW_API_KEY": DIFY_QNA_WORKFLOW_API_KEY,
            "DIFY_MONOLOGUE_WORKFLOW_API_KEY": DIFY_MONOLOGUE_WORKFLOW_API_KEY,
        }
        
        all_good = True
        
        for var_name, var_value in config_vars.items():
            if var_value:
                # Mask API keys for security
                if "API_KEY" in var_name and var_value:
                    masked_value = var_value[:8] + "..." + var_value[-4:] if len(var_value) > 12 else "***"
                    print(f"✅ {var_name}: {masked_value}")
                else:
                    print(f"✅ {var_name}: {var_value}")
            else:
                print(f"❌ {var_name}: NOT SET")
                all_good = False
        
        print("=" * 50)
        
        if all_good:
            print("🎉 Config module loaded all variables correctly!")
        else:
            print("⚠️  Some config variables are missing.")
        
        return all_good
        
    except Exception as e:
        print(f"❌ Failed to import config: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Dify API Configuration Test")
    print("=" * 60)
    
    # Test 1: Environment variables
    env_ok = test_env_variables()
    
    # Test 2: Config module
    config_ok = test_config_import()
    
    print("\n📋 Summary")
    print("=" * 60)
    
    if env_ok and config_ok:
        print("🎉 All tests passed! Dify API configuration is ready.")
        exit(0)
    else:
        print("❌ Some tests failed. Please fix the configuration issues.")
        exit(1)
