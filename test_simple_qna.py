#!/usr/bin/env python3
"""
Simple Q&A test to check parameter passing through the API.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def main():
    """Simple Q&A test."""
    print("🧪 Simple Q&A Test")
    print("=" * 40)
    
    try:
        # Create game
        print("1. Creating game...")
        game_response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/start",
            json={"script_id": "2", "user_id": "simple_test_user"},
            timeout=30
        )
        
        if game_response.status_code != 201:
            print(f"❌ Failed to create game: {game_response.status_code}")
            return False
        
        session_id = game_response.json()['data']['session_id']
        print(f"✅ Game created: {session_id}")
        
        # Ask question without history (should work)
        print("\n2. Asking question without history...")
        qna_response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
            json={
                "action_type": "qna",
                "character_id": "首席探长",
                "question": "你好",
                "questioner_id": "test_player",
                "user_id": "simple_test_user"
            },
            timeout=60
        )
        
        if qna_response.status_code != 200:
            print(f"❌ Q&A failed: {qna_response.status_code}")
            print(f"Response: {qna_response.text}")
            return False
        
        result = qna_response.json()
        if result.get("success"):
            answer = result.get('data', {}).get('answer', 'No answer')
            print(f"✅ Q&A completed: {answer[:100]}...")
            
            # Check for fallback error message
            if "抱歉，我暂时无法回答这个问题" in answer:
                print("❌ Got fallback error message")
                return False
            else:
                print("✅ Got proper AI response")
                return True
        else:
            print(f"❌ Q&A action failed: {result.get('error')}")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("🎉 Simple Q&A test passed!")
    else:
        print("❌ Simple Q&A test failed!")
    exit(0 if success else 1)
