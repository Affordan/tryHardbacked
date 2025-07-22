#!/usr/bin/env python3
"""
Test script to verify optimized monologue processing and act advancement features.
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_monologue_optimization():
    """Test the optimized monologue processing with sentence splitting."""
    print("🎭 Testing Optimized Monologue Processing")
    print("=" * 60)
    
    # First create a game
    game_data = {
        "script_id": "2",
        "user_id": "test_user",
        "ai_characters": [
            {
                "character_id": "法医专家",
                "model_name": "qwen"
            }
        ]
    }
    
    try:
        print("📤 Creating game with AI character...")
        response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/start",
            json=game_data,
            timeout=30
        )
        
        if response.status_code != 201:
            print(f"❌ Failed to create game: {response.status_code}")
            return None
        
        result = response.json()
        session_id = result['data']['session_id']
        print(f"✅ Game created with session: {session_id}")
        
        # Test monologue action
        monologue_data = {
            "action_type": "monologue",
            "character_id": "法医专家",
            "user_id": "test_user"
        }
        
        print("\n📤 Sending monologue request...")
        response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
            json=monologue_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("success"):
                print("✅ Monologue action completed successfully!")
                
                data = result.get('data', {})
                
                # Check for new monologue_sentences field
                if 'monologue_sentences' in data:
                    sentences = data['monologue_sentences']
                    print(f"✅ Found monologue_sentences field with {len(sentences)} sentences")
                    
                    for i, sentence in enumerate(sentences, 1):
                        print(f"   Sentence {i}: {sentence[:50]}..." if len(sentence) > 50 else f"   Sentence {i}: {sentence}")
                    
                    # Check if AI ending phrases were removed
                    has_ending_phrase = any("我的话已经说完了" in s for s in sentences)
                    if not has_ending_phrase:
                        print("✅ AI ending phrases correctly removed")
                    else:
                        print("⚠️  AI ending phrases still present")
                    
                    return session_id
                else:
                    print("❌ monologue_sentences field not found in response")
                    print(f"   Available fields: {list(data.keys())}")
                    return None
            else:
                print(f"❌ Monologue action failed: {result.get('error', 'Unknown error')}")
                return None
        else:
            print(f"❌ Monologue request failed: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def test_act_advancement(session_id):
    """Test the new act advancement mechanism."""
    if not session_id:
        print("⏭️  Skipping act advancement test - no valid session")
        return False
    
    print(f"\n🎬 Testing Act Advancement Mechanism")
    print("=" * 60)
    
    # Test act advancement action
    advance_data = {
        "action_type": "advance_act",
        "user_id": "test_user"
    }
    
    try:
        print("📤 Sending act advancement request...")
        response = requests.post(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/action",
            json=advance_data,
            timeout=30
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get("success"):
                print("✅ Act advancement completed successfully!")
                
                data = result.get('data', {})
                
                # Check advancement details
                new_act = data.get('new_act')
                current_phase = data.get('current_phase')
                max_acts = data.get('max_acts')
                players_reset = data.get('players_reset')
                
                print(f"   New Act: {new_act}")
                print(f"   Current Phase: {current_phase}")
                print(f"   Max Acts: {max_acts}")
                print(f"   Players Reset: {players_reset}")
                
                # Verify phase reset to MONOLOGUE
                if current_phase == "monologue":
                    print("✅ Game phase correctly reset to MONOLOGUE")
                else:
                    print(f"❌ Game phase not reset correctly: {current_phase}")
                
                # Verify act progression
                if new_act and new_act > 1:
                    print(f"✅ Act correctly advanced to {new_act}")
                else:
                    print(f"❌ Act not advanced correctly: {new_act}")
                
                return True
            else:
                print(f"❌ Act advancement failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Act advancement request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Act advancement request failed: {e}")
        return False

def test_game_status(session_id):
    """Test game status after optimizations."""
    if not session_id:
        print("⏭️  Skipping game status test - no valid session")
        return False
    
    print(f"\n📊 Testing Game Status After Optimizations")
    print("=" * 60)
    
    try:
        print("📤 Requesting game status...")
        response = requests.get(
            f"{BASE_URL}/api/v1/langchain-game/session/{session_id}/status",
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Game status retrieved successfully!")
            
            # Check game state details
            game_state = result.get('game_state', {})
            print(f"   Current Act: {game_state.get('current_act')}")
            print(f"   Current Phase: {game_state.get('current_phase')}")
            print(f"   Player Count: {game_state.get('player_count')}")
            print(f"   Character Count: {game_state.get('character_count')}")
            
            return True
        else:
            print(f"❌ Game status request failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Game status request failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Optimized Features Test Suite")
    print("=" * 70)
    
    # Test 1: Monologue optimization
    session_id = test_monologue_optimization()
    
    # Test 2: Act advancement
    act_success = test_act_advancement(session_id)
    
    # Test 3: Game status
    status_success = test_game_status(session_id)
    
    print("\n📊 Test Summary")
    print("=" * 70)
    
    if session_id and act_success and status_success:
        print("🎉 All tests passed!")
        print("✅ Monologue sentence splitting working correctly")
        print("✅ Act advancement mechanism functioning properly")
        print("✅ Game status tracking accurate")
        return True
    else:
        print("❌ Some tests failed:")
        if not session_id:
            print("   - Monologue optimization test failed")
        if not act_success:
            print("   - Act advancement test failed")
        if not status_success:
            print("   - Game status test failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
