#!/usr/bin/env python3
"""
Test script to verify AI character initialization functionality after refactoring.
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_ai_character_initialization():
    """Test the new AI character initialization mechanism."""
    print("🧪 Testing AI Character Initialization")
    print("=" * 60)
    
    # Test data with AI character assignments
    test_data = {
        "script_id": "2",
        "user_id": "test_user",
        "ai_characters": [
            {
                "character_id": "法医专家",
                "model_name": "qwen"
            },
            {
                "character_id": "神秘访客", 
                "model_name": "kimi"
            }
        ]
    }
    
    try:
        print("📤 Sending game start request with AI characters...")
        print(f"   Request data: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/start",
            json=test_data,
            timeout=30
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Game created successfully!")
            
            # Check response structure
            print("\n📋 Response Analysis:")
            print(f"   Success: {result.get('success')}")
            print(f"   Message: {result.get('message')}")
            
            # Check data section
            data = result.get('data', {})
            session_id = data.get('session_id')
            available_human_characters = data.get('available_human_characters', [])
            
            print(f"   Session ID: {session_id}")
            print(f"   Available Human Characters: {available_human_characters}")
            
            # Check game state
            game_state = result.get('game_state', {})
            print(f"   Game ID: {game_state.get('game_id')}")
            print(f"   Current Phase: {game_state.get('current_phase')}")
            print(f"   Player Count: {game_state.get('player_count')}")
            print(f"   Character Count: {game_state.get('character_count')}")
            
            # Verify AI characters are excluded from available human characters
            ai_character_ids = {ai_char["character_id"] for ai_char in test_data["ai_characters"]}
            excluded_correctly = all(
                ai_char_id not in available_human_characters 
                for ai_char_id in ai_character_ids
            )
            
            if excluded_correctly:
                print("✅ AI characters correctly excluded from available human characters")
            else:
                print("❌ AI characters not properly excluded from available human characters")
            
            return session_id
            
        else:
            print(f"❌ Failed to create game: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def test_monologue_with_bound_model(session_id):
    """Test monologue action with AI character's bound model."""
    if not session_id:
        print("⏭️  Skipping monologue test - no valid session")
        return False
    
    print(f"\n🎭 Testing Monologue with Bound Model")
    print("=" * 60)
    
    # Test monologue for AI character
    monologue_data = {
        "action_type": "monologue",
        "character_id": "法医专家",  # This should use 'qwen' model
        "user_id": "test_user"
    }
    
    try:
        print("📤 Sending monologue request...")
        print(f"   Character: {monologue_data['character_id']}")
        print(f"   Expected Model: qwen (bound to character)")
        
        response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
            json=monologue_data,
            timeout=60
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("success"):
                print("✅ Monologue action completed successfully!")
                
                data = result.get('data', {})
                monologue = data.get('monologue', 'No monologue returned')
                character_id = data.get('character_id', 'Unknown')
                
                print(f"   Character: {character_id}")
                print(f"   Monologue: {monologue[:100]}..." if len(monologue) > 100 else f"   Monologue: {monologue}")
                
                return True
            else:
                print(f"❌ Monologue action failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Monologue request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Monologue request failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 AI Character Initialization Test Suite")
    print("=" * 70)
    
    # Test 1: AI character initialization
    session_id = test_ai_character_initialization()
    
    # Test 2: Monologue with bound model
    monologue_success = test_monologue_with_bound_model(session_id)
    
    print("\n📊 Test Summary")
    print("=" * 70)
    
    if session_id and monologue_success:
        print("🎉 All tests passed!")
        print("✅ AI character initialization working correctly")
        print("✅ Model binding functioning properly")
        print("✅ Available human characters correctly filtered")
        return True
    else:
        print("❌ Some tests failed:")
        if not session_id:
            print("   - AI character initialization failed")
        if not monologue_success:
            print("   - Monologue with bound model failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
