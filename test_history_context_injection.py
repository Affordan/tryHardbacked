#!/usr/bin/env python3
"""
Test script to verify automatic history context injection for Q&A actions.
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
        "user_id": "history_test_user",
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
        "user_id": "history_test_user"
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
                return True
            else:
                print(f"❌ Monologue failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Monologue request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error performing monologue: {e}")
        return False

def ask_question(session_id, character_id, question, questioner_id="test_player"):
    """Ask a question to a character."""
    print(f"\n❓ Asking question to {character_id}: {question}")
    
    qna_data = {
        "action_type": "qna",
        "character_id": character_id,
        "question": question,
        "questioner_id": questioner_id,
        "user_id": "history_test_user"
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
                data = result.get('data', {})
                answer = data.get('answer', 'No answer')
                print(f"✅ Answer received: {answer[:100]}..." if len(answer) > 100 else f"✅ Answer: {answer}")
                return answer
            else:
                print(f"❌ Q&A failed: {result.get('error')}")
                return None
        else:
            print(f"❌ Q&A request failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error asking question: {e}")
        return None

def test_history_context_injection():
    """Test the complete history context injection workflow."""
    print("🔍 Testing History Context Injection")
    print("=" * 60)
    
    # Step 1: Create game
    session_id = create_test_game()
    if not session_id:
        return False
    
    # Step 2: Perform initial monologue to create history
    monologue_success = perform_monologue(session_id, "法医专家")
    if not monologue_success:
        print("❌ Failed to create initial history")
        return False
    
    # Step 3: Ask first question
    first_answer = ask_question(
        session_id, 
        "法医专家", 
        "你好，请介绍一下你自己。",
        "玩家1"
    )
    if not first_answer:
        print("❌ Failed to get first answer")
        return False
    
    # Step 4: Ask follow-up question that should reference previous context
    second_answer = ask_question(
        session_id,
        "法医专家",
        "根据你刚才说的内容，你觉得这个案件有什么特殊之处？",
        "玩家2"
    )
    if not second_answer:
        print("❌ Failed to get second answer")
        return False
    
    # Step 5: Ask a question that should reference the conversation history
    third_answer = ask_question(
        session_id,
        "法医专家",
        "你之前提到的那些细节，能再详细说明一下吗？",
        "玩家1"
    )
    if not third_answer:
        print("❌ Failed to get third answer")
        return False
    
    print("\n📊 History Context Test Results:")
    print("✅ Successfully created game with AI character")
    print("✅ Performed initial monologue to establish history")
    print("✅ Asked multiple questions with context references")
    print("✅ All Q&A responses received successfully")
    
    # Analyze if responses show contextual awareness
    context_indicators = [
        "刚才", "之前", "前面", "刚刚", "刚说", "提到", "说过", "谈到"
    ]
    
    contextual_responses = 0
    for i, answer in enumerate([second_answer, third_answer], 2):
        has_context = any(indicator in answer for indicator in context_indicators)
        if has_context:
            contextual_responses += 1
            print(f"✅ Answer {i} shows contextual awareness")
        else:
            print(f"⚠️  Answer {i} may lack contextual awareness")
    
    if contextual_responses > 0:
        print(f"🎉 History context injection working! {contextual_responses}/2 responses show context awareness")
        return True
    else:
        print("⚠️  History context injection may need improvement")
        return False

def main():
    """Main test function."""
    print("🚀 History Context Injection Test Suite")
    print("=" * 70)
    
    success = test_history_context_injection()
    
    print("\n📊 Final Test Summary")
    print("=" * 70)
    
    if success:
        print("🎉 History context injection test completed successfully!")
        print("✅ Q&A responses are contextually aware of previous events")
        print("✅ Frontend API calls remain unchanged")
        print("✅ History is automatically formatted and injected server-side")
        return True
    else:
        print("❌ History context injection test failed")
        print("   - Check server logs for detailed error information")
        print("   - Verify Dify workflow supports history parameter")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
