#!/usr/bin/env python3
"""
Complete integration test for script data and AI character initialization.
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_script_data_integrity():
    """Test script data integrity and character availability."""
    print("📚 Testing Script Data Integrity")
    print("=" * 60)
    
    try:
        # Test script list endpoint
        print("📤 Fetching script list...")
        response = requests.get(f"{BASE_URL}/api/v1/scripts", timeout=30)
        
        if response.status_code == 200:
            response_data = response.json()
            scripts = response_data.get('scripts', [])
            print(f"✅ Found {len(scripts)} scripts")
            
            # Check script 1 (午夜图书馆)
            script1 = next((s for s in scripts if s['id'] == '1'), None)
            if script1:
                print(f"📖 Script 1: {script1['title']}")
                print(f"   Players: {script1['players']}")
                print(f"   Characters: {len(script1.get('characters', []))}")
                
                if len(script1.get('characters', [])) == 6:
                    print("✅ Script 1 has complete character data (6 characters)")
                else:
                    print(f"❌ Script 1 character count mismatch: {len(script1.get('characters', []))}")
            
            # Check script 2 (雾都疑案)
            script2 = next((s for s in scripts if s['id'] == '2'), None)
            if script2:
                print(f"\n📖 Script 2: {script2['title']}")
                print(f"   Players: {script2['players']}")
                print(f"   Characters: {len(script2.get('characters', []))}")
                
                character_names = [char['name'] for char in script2.get('characters', [])]
                print(f"   Character names: {character_names}")
                
                # Check for test script compatibility
                required_chars = ["法医专家", "神秘访客"]
                all_found = all(char in character_names for char in required_chars)
                
                if all_found:
                    print("✅ Script 2 contains all required test characters")
                    return True
                else:
                    print("❌ Script 2 missing required test characters")
                    return False
            
        else:
            print(f"❌ Failed to fetch scripts: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_ai_character_initialization():
    """Test AI character initialization with updated script data."""
    print("\n🤖 Testing AI Character Initialization")
    print("=" * 60)
    
    # Test data with AI character assignments
    test_data = {
        "script_id": "2",
        "user_id": "integration_test_user",
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
        print("📤 Creating game with AI characters...")
        print(f"   Script: 雾都疑案 (ID: 2)")
        print(f"   AI Characters: {[ai['character_id'] for ai in test_data['ai_characters']]}")
        
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
            data = result.get('data', {})
            session_id = data.get('session_id')
            available_human_characters = data.get('available_human_characters', [])
            
            print(f"   Session ID: {session_id}")
            print(f"   Available Human Characters: {available_human_characters}")
            
            # Verify AI characters are excluded from available human characters
            ai_character_ids = {ai_char["character_id"] for ai_char in test_data["ai_characters"]}
            excluded_correctly = all(
                ai_char_id not in available_human_characters 
                for ai_char_id in ai_character_ids
            )
            
            if excluded_correctly:
                print("✅ AI characters correctly excluded from available human characters")
            else:
                print("❌ AI characters not properly excluded")
            
            # Check expected human characters
            expected_human_chars = ["首席探长", "贵族夫人", "私家侦探", "报社记者"]
            human_chars_correct = all(
                char in available_human_characters 
                for char in expected_human_chars
            )
            
            if human_chars_correct:
                print("✅ All expected human characters are available")
            else:
                print(f"❌ Some expected human characters missing")
                print(f"   Expected: {expected_human_chars}")
                print(f"   Available: {available_human_characters}")
            
            return session_id, excluded_correctly and human_chars_correct
            
        else:
            print(f"❌ Failed to create game: {response.status_code}")
            print(f"   Response: {response.text}")
            return None, False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None, False

def test_optimized_features(session_id):
    """Test optimized monologue and act advancement features."""
    if not session_id:
        print("⏭️  Skipping optimized features test - no valid session")
        return False
    
    print(f"\n🎭 Testing Optimized Features")
    print("=" * 60)
    
    # Test monologue with AI character
    monologue_data = {
        "action_type": "monologue",
        "character_id": "法医专家",  # AI character with qwen model
        "user_id": "integration_test_user"
    }
    
    try:
        print("📤 Testing monologue with AI character...")
        response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
            json=monologue_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("success"):
                data = result.get('data', {})
                
                # Check for monologue_sentences field
                if 'monologue_sentences' in data:
                    sentences = data['monologue_sentences']
                    print(f"✅ Monologue sentences: {len(sentences)} sentences")
                    
                    # Test act advancement
                    advance_data = {
                        "action_type": "advance_act",
                        "user_id": "integration_test_user"
                    }
                    
                    print("📤 Testing act advancement...")
                    response = requests.post(
                        f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
                        json=advance_data,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result.get("success"):
                            data = result.get('data', {})
                            new_act = data.get('new_act')
                            current_phase = data.get('current_phase')
                            
                            print(f"✅ Act advanced to: {new_act}")
                            print(f"✅ Phase reset to: {current_phase}")
                            
                            return True
                        else:
                            print(f"❌ Act advancement failed: {result.get('error')}")
                    else:
                        print(f"❌ Act advancement request failed: {response.status_code}")
                else:
                    print("❌ monologue_sentences field not found")
            else:
                print(f"❌ Monologue failed: {result.get('error')}")
        else:
            print(f"❌ Monologue request failed: {response.status_code}")
        
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Main integration test function."""
    print("🚀 Complete Integration Test Suite")
    print("=" * 70)
    
    # Test 1: Script data integrity
    script_data_ok = test_script_data_integrity()
    
    # Test 2: AI character initialization
    session_id, ai_init_ok = test_ai_character_initialization()
    
    # Test 3: Optimized features
    optimized_features_ok = test_optimized_features(session_id)
    
    print("\n📊 Integration Test Summary")
    print("=" * 70)
    
    if script_data_ok and ai_init_ok and optimized_features_ok:
        print("🎉 All integration tests passed!")
        print("✅ Script data integrity verified")
        print("✅ AI character initialization working correctly")
        print("✅ Optimized features functioning properly")
        print("✅ Complete system integration successful")
        return True
    else:
        print("❌ Some integration tests failed:")
        if not script_data_ok:
            print("   - Script data integrity test failed")
        if not ai_init_ok:
            print("   - AI character initialization test failed")
        if not optimized_features_ok:
            print("   - Optimized features test failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
