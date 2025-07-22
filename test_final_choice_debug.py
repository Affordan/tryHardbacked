#!/usr/bin/env python3
"""
Debug test for final_choice action to check data transmission.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def create_test_game():
    """Create a test game."""
    test_data = {
        "script_id": "2",
        "user_id": "debug_test_user"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/langchain-game/start", json=test_data, timeout=30)
    
    if response.status_code == 201:
        result = response.json()
        session_id = result['data']['session_id']
        print(f"✅ Game created: {session_id}")
        return session_id
    else:
        print(f"❌ Failed to create game: {response.status_code}")
        return None

def test_final_choice_debug(session_id, tell_truth_value):
    """Test final choice with specific tell_truth value."""
    print(f"\n🔍 Testing tell_truth={tell_truth_value}")
    
    final_choice_data = {
        "action_type": "final_choice",
        "player_id": "debug_player",
        "tell_truth": tell_truth_value,
        "user_id": "debug_test_user"
    }
    
    print(f"📤 Sending data: {json.dumps(final_choice_data, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
        json=final_choice_data,
        timeout=30
    )
    
    print(f"📥 Response status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"📋 Response data: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("success"):
            data = result.get('data', {})
            received_tell_truth = data.get('tell_truth')
            choice = data.get('choice')
            
            print(f"✅ Success!")
            print(f"   Sent tell_truth: {tell_truth_value} (type: {type(tell_truth_value)})")
            print(f"   Received tell_truth: {received_tell_truth} (type: {type(received_tell_truth)})")
            print(f"   Choice description: {choice}")
            
            return received_tell_truth == tell_truth_value
        else:
            print(f"❌ Action failed: {result.get('error')}")
            return False
    else:
        print(f"❌ Request failed: {response.text}")
        return False

def main():
    """Main debug function."""
    print("🔍 Final Choice Debug Test")
    print("=" * 50)
    
    # Test with tell_truth=True
    session_id1 = create_test_game()
    if session_id1:
        result1 = test_final_choice_debug(session_id1, True)
    
    # Test with tell_truth=False
    session_id2 = create_test_game()
    if session_id2:
        result2 = test_final_choice_debug(session_id2, False)
    
    print(f"\n📊 Debug Results:")
    print(f"   tell_truth=True test: {'✅ PASS' if result1 else '❌ FAIL'}")
    print(f"   tell_truth=False test: {'✅ PASS' if result2 else '❌ FAIL'}")

if __name__ == "__main__":
    main()
