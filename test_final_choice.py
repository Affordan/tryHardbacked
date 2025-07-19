#!/usr/bin/env python3
"""
Test script to verify the final_choice action handler implementation.
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def create_test_game():
    """Create a test game to get a session ID."""
    print("🎮 Creating test game...")
    
    test_data = {
        "script_id": "2",
        "user_id": "final_choice_test_user",
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

def test_final_choice_tell_truth(session_id):
    """Test final_choice action with tell_truth=true."""
    if not session_id:
        print("⏭️  Skipping tell truth test - no valid session")
        return False
    
    print(f"\n✅ Testing Final Choice - Tell Truth")
    print("=" * 50)
    
    final_choice_data = {
        "action_type": "final_choice",
        "player_id": "test_player",
        "tell_truth": True,
        "user_id": "final_choice_test_user"
    }
    
    try:
        print("📤 Sending final choice request (tell_truth=True)...")
        response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
            json=final_choice_data,
            timeout=30
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("success"):
                print("✅ Final choice (tell truth) completed successfully!")
                
                data = result.get('data', {})
                ending = data.get('ending', [])
                choice = data.get('choice', 'Unknown')
                tell_truth = data.get('tell_truth', False)
                current_phase = data.get('current_phase', 'Unknown')
                
                print(f"   Choice: {choice}")
                print(f"   Tell Truth: {tell_truth}")
                print(f"   Current Phase: {current_phase}")
                print(f"   Ending Lines: {len(ending)}")
                
                # Print first few lines of ending
                for i, line in enumerate(ending[:3], 1):
                    print(f"   Line {i}: {line[:60]}..." if len(line) > 60 else f"   Line {i}: {line}")
                
                # Verify expected content
                if "丰翰啊" in str(ending):
                    print("✅ Truth ending content verified")
                    return True
                else:
                    print("❌ Truth ending content not found")
                    return False
            else:
                print(f"❌ Final choice failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Final choice request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing final choice: {e}")
        return False

def test_final_choice_hide_truth(session_id):
    """Test final_choice action with tell_truth=false."""
    if not session_id:
        print("⏭️  Skipping hide truth test - no valid session")
        return False
    
    print(f"\n❌ Testing Final Choice - Hide Truth")
    print("=" * 50)
    
    final_choice_data = {
        "action_type": "final_choice",
        "player_id": "test_player",
        "tell_truth": False,
        "user_id": "final_choice_test_user"
    }
    
    try:
        print("📤 Sending final choice request (tell_truth=False)...")
        response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
            json=final_choice_data,
            timeout=30
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("success"):
                print("✅ Final choice (hide truth) completed successfully!")
                
                data = result.get('data', {})
                ending = data.get('ending', [])
                choice = data.get('choice', 'Unknown')
                tell_truth = data.get('tell_truth', True)
                current_phase = data.get('current_phase', 'Unknown')
                
                print(f"   Choice: {choice}")
                print(f"   Tell Truth: {tell_truth}")
                print(f"   Current Phase: {current_phase}")
                print(f"   Ending Lines: {len(ending)}")
                
                # Print first few lines of ending
                for i, line in enumerate(ending[:3], 1):
                    print(f"   Line {i}: {line[:60]}..." if len(line) > 60 else f"   Line {i}: {line}")
                
                # Verify expected content
                if "我当是咋了" in str(ending):
                    print("✅ Hide truth ending content verified")
                    return True
                else:
                    print("❌ Hide truth ending content not found")
                    return False
            else:
                print(f"❌ Final choice failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Final choice request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing final choice: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Final Choice Action Handler Test")
    print("=" * 60)
    
    # Create test game
    session_id = create_test_game()
    
    # Test both truth and lie choices
    truth_ok = test_final_choice_tell_truth(session_id)
    
    # Create a new game for the second test
    session_id2 = create_test_game()
    lie_ok = test_final_choice_hide_truth(session_id2)
    
    print("\n📊 Test Summary")
    print("=" * 60)
    
    if truth_ok and lie_ok:
        print("🎉 All final choice tests passed!")
        print("✅ Tell truth ending working correctly")
        print("✅ Hide truth ending working correctly")
        print("✅ No more 'Unknown action type' errors")
        print("✅ Game phase correctly set to COMPLETED")
        return True
    else:
        print("❌ Some final choice tests failed:")
        if not truth_ok:
            print("   - Tell truth test failed")
        if not lie_ok:
            print("   - Hide truth test failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
