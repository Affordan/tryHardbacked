#!/usr/bin/env python3
"""
Test script to verify the status endpoint is working correctly.
"""

import requests
import json
import traceback

BASE_URL = "http://127.0.0.1:8000"

def create_test_game():
    """Create a test game to get a session ID."""
    print("🎮 Creating test game...")
    
    test_data = {
        "script_id": "2",
        "user_id": "status_test_user",
        "ai_characters": [
            {
                "character_id": "法医专家",
                "model_name": "qwen"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/start",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 201:
            result = response.json()
            session_id = result['data']['session_id']
            print(f"✅ Game created with session: {session_id}")
            return session_id
        else:
            print(f"❌ Failed to create game: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating game: {e}")
        return None

def test_status_endpoint(session_id):
    """Test the status endpoint."""
    if not session_id:
        print("⏭️  Skipping status test - no valid session")
        return False
    
    print(f"\n📊 Testing Status Endpoint")
    print("=" * 50)
    
    try:
        print(f"📤 Requesting status for session: {session_id}")
        response = requests.get(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/status",
            timeout=30
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Status endpoint working correctly!")
            
            # Check response structure
            game_state = result.get('game_state', {})
            progress = result.get('progress', {})
            available_actions = result.get('available_actions', [])
            
            print(f"   Game ID: {game_state.get('game_id')}")
            print(f"   Current Act: {game_state.get('current_act')}")
            print(f"   Current Phase: {game_state.get('current_phase')}")
            print(f"   Player Count: {game_state.get('player_count')}")
            print(f"   Character Count: {game_state.get('character_count')}")
            print(f"   Progress: {progress}")
            print(f"   Available Actions: {len(available_actions)}")
            
            return True
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing status endpoint: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False

def test_status_with_history(session_id):
    """Test the status endpoint with history."""
    if not session_id:
        print("⏭️  Skipping status with history test - no valid session")
        return False
    
    print(f"\n📚 Testing Status Endpoint with History")
    print("=" * 50)
    
    try:
        print(f"📤 Requesting status with history for session: {session_id}")
        response = requests.get(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/status?include_history=true&max_log_entries=10",
            timeout=30
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Status with history endpoint working correctly!")
            
            # Check history fields
            recent_log_entries = result.get('recent_log_entries', [])
            qna_history = result.get('qna_history', [])
            mission_submissions = result.get('mission_submissions', [])
            
            print(f"   Recent Log Entries: {len(recent_log_entries)}")
            print(f"   Q&A History: {len(qna_history)}")
            print(f"   Mission Submissions: {len(mission_submissions)}")
            
            return True
        else:
            print(f"❌ Status with history endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing status with history endpoint: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False

def main():
    """Main test function."""
    print("🚀 Status Endpoint Test Suite")
    print("=" * 60)
    
    # Create test game
    session_id = create_test_game()
    
    # Test basic status endpoint
    status_ok = test_status_endpoint(session_id)
    
    # Test status endpoint with history
    status_history_ok = test_status_with_history(session_id)
    
    print("\n📊 Test Summary")
    print("=" * 60)
    
    if status_ok and status_history_ok:
        print("🎉 All status endpoint tests passed!")
        print("✅ Basic status endpoint working")
        print("✅ Status with history endpoint working")
        print("✅ No .value attribute errors detected")
        return True
    else:
        print("❌ Some status endpoint tests failed:")
        if not status_ok:
            print("   - Basic status endpoint test failed")
        if not status_history_ok:
            print("   - Status with history endpoint test failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
