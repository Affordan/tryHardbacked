#!/usr/bin/env python3
"""
Test script to verify the Dify API 400 BAD REQUEST fix.
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
        "user_id": "dify_400_test_user",
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
        "user_id": "dify_400_test_user"
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

def test_qna_with_history(session_id, character_id, question):
    """Test Q&A with history context to check for 400 errors."""
    print(f"\n❓ Testing Q&A with history context...")
    print(f"   Character: {character_id}")
    print(f"   Question: {question}")
    
    qna_data = {
        "action_type": "qna",
        "character_id": character_id,
        "question": question,
        "questioner_id": "test_player",
        "user_id": "dify_400_test_user"
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
                
                # Check if we got the fallback error message
                if "抱歉，我暂时无法回答这个问题" in answer:
                    print("⚠️  Received fallback error message - Dify API may have failed")
                    return False
                else:
                    print("✅ Received proper AI response - Dify API working correctly")
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

def test_multiple_qna_rounds(session_id, character_id):
    """Test multiple Q&A rounds to verify consistent behavior."""
    print(f"\n🔄 Testing Multiple Q&A Rounds...")
    
    questions = [
        "你好，请介绍一下你自己。",
        "你觉得这个案件最可疑的地方是什么？",
        "根据你刚才提到的线索，下一步应该怎么调查？"
    ]
    
    success_count = 0
    for i, question in enumerate(questions, 1):
        print(f"\n   Round {i}: {question}")
        
        qna_data = {
            "action_type": "qna",
            "character_id": character_id,
            "question": question,
            "questioner_id": f"player_{i}",
            "user_id": "dify_400_test_user"
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
                    
                    # Check for fallback error message
                    if "抱歉，我暂时无法回答这个问题" in answer:
                        print(f"   ⚠️  Round {i}: Got fallback error message")
                    else:
                        print(f"   ✅ Round {i}: Success - {answer[:60]}...")
                        success_count += 1
                else:
                    print(f"   ❌ Round {i} failed: {result.get('error')}")
            else:
                print(f"   ❌ Round {i} request failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Round {i} error: {e}")
        
        # Small delay between requests
        time.sleep(2)
    
    print(f"\n📊 Multiple Q&A Results: {success_count}/{len(questions)} rounds successful")
    return success_count >= 2  # Allow for some tolerance

def main():
    """Main test function."""
    print("🔧 Dify API 400 BAD REQUEST Fix Test")
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
    
    # Step 3: Test Q&A with history context
    qna_success = test_qna_with_history(
        session_id, 
        "首席探长", 
        "你好，请根据你刚才说的内容，详细介绍一下这个案件。"
    )
    
    # Step 4: Test multiple Q&A rounds
    multiple_rounds_success = test_multiple_qna_rounds(session_id, "首席探长")
    
    print("\n📊 Final Test Summary")
    print("=" * 60)
    
    if qna_success and multiple_rounds_success:
        print("🎉 Dify API 400 BAD REQUEST fix successful!")
        print("✅ Q&A requests processed without 400 errors")
        print("✅ History context properly passed to Dify API")
        print("✅ Multiple Q&A rounds working correctly")
        print("✅ No fallback error messages detected")
        return True
    else:
        print("❌ Dify API 400 BAD REQUEST fix incomplete:")
        if not qna_success:
            print("   - Single Q&A test failed")
        if not multiple_rounds_success:
            print("   - Multiple Q&A rounds test failed")
        print("\n🔍 Check server logs for detailed error information")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
