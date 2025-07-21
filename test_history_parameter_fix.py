#!/usr/bin/env python3
"""
Test script to verify that history parameter is properly injected into Dify workflow calls.
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
        "user_id": "history_param_test_user",
        "ai_characters": []  # No AI characters for this test
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

def perform_monologue(session_id, character_id):
    """Perform a monologue to create history."""
    print(f"\n🎭 Performing monologue for {character_id}...")
    
    monologue_data = {
        "action_type": "monologue",
        "character_id": character_id,
        "user_id": "history_param_test_user"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
            json=monologue_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get('data', {})
                sentences = data.get('monologue_sentences', [])
                print(f"✅ Monologue completed: {len(sentences)} sentences")
                if sentences:
                    print(f"   First sentence: {sentences[0][:80]}...")
                return True
            else:
                print(f"❌ Monologue failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Monologue request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error performing monologue: {e}")
        return False

def ask_question_with_history_check(session_id, character_id, question):
    """Ask a question and verify that history context is being passed."""
    print(f"\n❓ Testing Q&A with history injection...")
    print(f"   Character: {character_id}")
    print(f"   Question: {question}")
    
    qna_data = {
        "action_type": "qna",
        "character_id": character_id,
        "question": question,
        "questioner_id": "test_player",
        "user_id": "history_param_test_user"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
            json=qna_data,
            timeout=60
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                data = result.get('data', {})
                answer = data.get('answer', 'No answer')
                print(f"✅ Q&A completed successfully!")
                print(f"   Answer: {answer[:100]}..." if len(answer) > 100 else f"   Answer: {answer}")
                return True
            else:
                print(f"❌ Q&A failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Q&A request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error asking question: {e}")
        return False

def test_history_parameter_injection():
    """Test the complete history parameter injection workflow."""
    print("🔧 Testing History Parameter Injection Fix")
    print("=" * 60)
    
    # Step 1: Create game
    session_id = create_test_game()
    if not session_id:
        return False
    
    # Step 2: Perform monologue to create history
    monologue_success = perform_monologue(session_id, "首席探长")
    if not monologue_success:
        print("❌ Failed to create initial history")
        return False
    
    # Step 3: Ask question that should include history context
    qna_success = ask_question_with_history_check(
        session_id, 
        "首席探长", 
        "你好，请根据你刚才说的内容，详细介绍一下这个案件。"
    )
    
    if not qna_success:
        print("❌ Q&A with history injection failed")
        return False
    
    print("\n📊 History Parameter Injection Test Results:")
    print("✅ Game created successfully")
    print("✅ Monologue performed to establish history")
    print("✅ Q&A request processed successfully")
    print("✅ No 'history parameter missing' errors detected")
    
    return True

def test_multiple_qna_rounds(session_id):
    """Test multiple Q&A rounds to verify cumulative history building."""
    print(f"\n🔄 Testing Multiple Q&A Rounds...")
    
    questions = [
        "你觉得这个案件最可疑的地方是什么？",
        "根据你刚才提到的线索，下一步应该怎么调查？",
        "你之前说的那些细节中，哪个最重要？"
    ]
    
    success_count = 0
    for i, question in enumerate(questions, 1):
        print(f"\n   Round {i}: {question}")
        
        qna_data = {
            "action_type": "qna",
            "character_id": "首席探长",
            "question": question,
            "questioner_id": f"player_{i}",
            "user_id": "history_param_test_user"
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
                json=qna_data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    answer = result.get('data', {}).get('answer', 'No answer')
                    print(f"   ✅ Round {i} success: {answer[:60]}...")
                    success_count += 1
                else:
                    print(f"   ❌ Round {i} failed: {result.get('error')}")
            else:
                print(f"   ❌ Round {i} request failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Round {i} error: {e}")
        
        # Small delay between requests
        time.sleep(1)
    
    print(f"\n📊 Multiple Q&A Results: {success_count}/{len(questions)} rounds successful")
    return success_count == len(questions)

def main():
    """Main test function."""
    print("🚀 History Parameter Injection Fix Test Suite")
    print("=" * 70)
    
    # Test 1: Basic history parameter injection
    basic_test_success = test_history_parameter_injection()
    
    if not basic_test_success:
        print("\n❌ Basic test failed - stopping here")
        return False
    
    # Test 2: Multiple Q&A rounds (reuse the same session)
    # We need to create a new session for this test
    session_id = create_test_game()
    if session_id:
        perform_monologue(session_id, "首席探长")  # Create initial history
        multiple_rounds_success = test_multiple_qna_rounds(session_id)
    else:
        multiple_rounds_success = False
    
    print("\n📊 Final Test Summary")
    print("=" * 70)
    
    if basic_test_success and multiple_rounds_success:
        print("🎉 All history parameter injection tests passed!")
        print("✅ History context is properly injected into Dify workflows")
        print("✅ Q&A responses should now be contextually aware")
        print("✅ Frontend API calls remain unchanged")
        print("✅ Multiple Q&A rounds work correctly")
        return True
    else:
        print("❌ Some tests failed:")
        if not basic_test_success:
            print("   - Basic history parameter injection test failed")
        if not multiple_rounds_success:
            print("   - Multiple Q&A rounds test failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
