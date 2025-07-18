#!/usr/bin/env python3
"""
Test script to verify monologue API functionality after Dify configuration fix.
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_start_game():
    """Test starting a new game."""
    print("🎮 Testing game start...")
    
    url = f"{BASE_URL}/api/v1/langchain-game/start"
    data = {
        "script_id": "1",
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Game started successfully!")
        print(f"   Session ID: {result['game_state']['session_id']}")
        print(f"   Game ID: {result['game_state']['game_id']}")
        
        return result['game_state']['session_id']
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to start game: {e}")
        return None

def test_monologue_action(session_id):
    """Test monologue action."""
    print(f"\n🎭 Testing monologue action for session {session_id}...")
    
    url = f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action"
    data = {
        "action_type": "monologue",
        "character_id": "张三",
        "model_name": "gpt-3.5-turbo",
        "user_id": "test_user"
    }
    
    try:
        print("   Sending monologue request...")
        response = requests.post(url, json=data, timeout=60)  # Longer timeout for AI response
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("success"):
            print("✅ Monologue action completed successfully!")
            print(f"   Character: {result['data'].get('character_id', 'Unknown')}")
            monologue = result['data'].get('monologue', 'No monologue returned')
            print(f"   Monologue: {monologue[:100]}..." if len(monologue) > 100 else f"   Monologue: {monologue}")
            return True
        else:
            print(f"❌ Monologue action failed: {result.get('error', 'Unknown error')}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Monologue request timed out (this might indicate API key issues)")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to execute monologue: {e}")
        return False

def test_health_check():
    """Test basic health check."""
    print("🏥 Testing health check...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Health check passed: {result['message']}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Dify Monologue API Test")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health_check():
        print("❌ Server is not responding. Please check if it's running.")
        return False
    
    # Test 2: Start game
    session_id = test_start_game()
    if not session_id:
        print("❌ Cannot proceed without a valid game session.")
        return False
    
    # Test 3: Monologue action
    monologue_success = test_monologue_action(session_id)
    
    print("\n📋 Test Summary")
    print("=" * 50)
    
    if monologue_success:
        print("🎉 All tests passed! Monologue API is working correctly.")
        print("✅ Dify API key configuration is correct.")
        print("✅ Environment variables are loaded properly.")
        return True
    else:
        print("❌ Monologue test failed. Check the following:")
        print("   1. Dify API key configuration")
        print("   2. Network connectivity to Dify API")
        print("   3. Server logs for detailed error messages")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
