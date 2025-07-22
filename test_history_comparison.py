#!/usr/bin/env python3
"""
Test to compare Q&A with and without history context.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_qna_without_history():
    """Test Q&A without history context."""
    print("🧪 Testing Q&A without history...")
    
    try:
        # Create game
        game_response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/start",
            json={"script_id": "2", "user_id": "no_history_test"},
            timeout=30
        )
        
        if game_response.status_code != 201:
            print(f"❌ Failed to create game: {game_response.status_code}")
            return False
        
        session_id = game_response.json()['data']['session_id']
        print(f"✅ Game created: {session_id}")
        
        # Ask question immediately (no history)
        qna_response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
            json={
                "action_type": "qna",
                "character_id": "首席探长",
                "question": "你好，请介绍一下你自己。",
                "questioner_id": "test_player",
                "user_id": "no_history_test"
            },
            timeout=60
        )
        
        if qna_response.status_code != 200:
            print(f"❌ Q&A failed: {qna_response.status_code}")
            return False
        
        result = qna_response.json()
        if result.get("success"):
            answer = result.get('data', {}).get('answer', 'No answer')
            print(f"✅ Q&A without history: {answer[:80]}...")
            
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

def test_qna_with_history():
    """Test Q&A with history context."""
    print("\n🧪 Testing Q&A with history...")
    
    try:
        # Create game
        game_response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/start",
            json={"script_id": "2", "user_id": "with_history_test"},
            timeout=30
        )
        
        if game_response.status_code != 201:
            print(f"❌ Failed to create game: {game_response.status_code}")
            return False
        
        session_id = game_response.json()['data']['session_id']
        print(f"✅ Game created: {session_id}")
        
        # Perform monologue to create history
        print("   Creating history with monologue...")
        monologue_response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
            json={
                "action_type": "monologue",
                "character_id": "首席探长",
                "user_id": "with_history_test"
            },
            timeout=60
        )
        
        if monologue_response.status_code != 200:
            print(f"❌ Monologue failed: {monologue_response.status_code}")
            return False
        
        print("   ✅ Monologue completed")
        
        # Ask question with history
        qna_response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
            json={
                "action_type": "qna",
                "character_id": "首席探长",
                "question": "你好，请介绍一下你自己。",
                "questioner_id": "test_player",
                "user_id": "with_history_test"
            },
            timeout=60
        )
        
        if qna_response.status_code != 200:
            print(f"❌ Q&A failed: {qna_response.status_code}")
            return False
        
        result = qna_response.json()
        if result.get("success"):
            answer = result.get('data', {}).get('answer', 'No answer')
            print(f"✅ Q&A with history: {answer[:80]}...")
            
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

def main():
    """Main test function."""
    print("🔍 History Context Comparison Test")
    print("=" * 50)
    
    # Test without history
    no_history_ok = test_qna_without_history()
    
    # Test with history
    with_history_ok = test_qna_with_history()
    
    print("\n📊 Test Summary")
    print("=" * 50)
    
    if no_history_ok and with_history_ok:
        print("🎉 Both tests passed!")
        print("✅ Q&A without history: Working")
        print("✅ Q&A with history: Working")
        print("✅ History parameter injection fix successful!")
        return True
    else:
        print("❌ Some tests failed:")
        if not no_history_ok:
            print("   - Q&A without history failed")
        if not with_history_ok:
            print("   - Q&A with history failed")
        
        if no_history_ok and not with_history_ok:
            print("\n🔍 Issue is specifically with history parameter injection")
        elif not no_history_ok and with_history_ok:
            print("\n🔍 Issue is with basic Q&A functionality")
        else:
            print("\n🔍 Issue is with overall Q&A system")
        
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
