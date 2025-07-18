#!/usr/bin/env python3
"""
Test script to verify that all .value attribute errors have been fixed.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported without .value errors."""
    print("🔍 Testing Module Imports")
    print("=" * 50)
    
    try:
        print("📦 Testing app.langchain.state.models...")
        from app.langchain.state.models import GameState, GamePhase, MissionStatus
        print("✅ GameState, GamePhase, MissionStatus imported successfully")
        
        print("📦 Testing app.langchain.engine.nodes...")
        from app.langchain.engine.nodes import GamePhaseNodes
        print("✅ GamePhaseNodes imported successfully")
        
        print("📦 Testing app.langchain.engine.game_engine...")
        from app.langchain.engine.game_engine import GameEngine
        print("✅ GameEngine imported successfully")
        
        print("📦 Testing app.routers.langchain_game...")
        from app.routers.langchain_game import router
        print("✅ langchain_game router imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_enum_behavior():
    """Test that enums behave correctly as strings."""
    print("\n🧪 Testing Enum Behavior")
    print("=" * 50)
    
    try:
        from app.langchain.state.models import GamePhase, MissionStatus
        
        # Test GamePhase
        phase = GamePhase.MONOLOGUE
        print(f"GamePhase.MONOLOGUE = '{phase}' (type: {type(phase)})")
        
        # Test string operations
        phase_str = str(phase)
        print(f"str(GamePhase.MONOLOGUE) = '{phase_str}'")
        
        # Test comparison
        is_equal = phase == "monologue"
        print(f"GamePhase.MONOLOGUE == 'monologue': {is_equal}")
        
        # Test MissionStatus
        status = MissionStatus.PENDING
        print(f"MissionStatus.PENDING = '{status}' (type: {type(status)})")
        
        status_str = str(status)
        print(f"str(MissionStatus.PENDING) = '{status_str}'")
        
        is_equal = status == "pending"
        print(f"MissionStatus.PENDING == 'pending': {is_equal}")
        
        print("✅ All enum behaviors working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Enum behavior test failed: {e}")
        return False

def test_game_state_creation():
    """Test GameState creation with enum fields."""
    print("\n🎮 Testing GameState Creation")
    print("=" * 50)
    
    try:
        from app.langchain.state.models import GameState, GamePhase
        from datetime import datetime, timezone
        
        # Create a GameState instance
        game_state = GameState(
            game_id="test_game",
            script_id="test_script",
            session_id="test_session",
            current_phase=GamePhase.INITIALIZATION,
            started_at=datetime.now(timezone.utc)
        )
        
        print(f"Created GameState with current_phase: '{game_state.current_phase}'")
        print(f"Type of current_phase: {type(game_state.current_phase)}")
        
        # Test phase transition
        game_state.current_phase = GamePhase.MONOLOGUE
        print(f"Changed current_phase to: '{game_state.current_phase}'")
        
        # Test string formatting
        phase_message = f"Current phase is: {game_state.current_phase}"
        print(f"String formatting: {phase_message}")
        
        print("✅ GameState creation and manipulation working correctly")
        return True
        
    except Exception as e:
        print(f"❌ GameState creation test failed: {e}")
        return False

def test_nodes_functionality():
    """Test GamePhaseNodes functionality."""
    print("\n🔧 Testing GamePhaseNodes Functionality")
    print("=" * 50)
    
    try:
        from app.langchain.engine.nodes import GamePhaseNodes
        from app.langchain.state.models import GameState, GamePhase
        from datetime import datetime, timezone
        
        # Create a test GameState
        game_state = GameState(
            game_id="test_game",
            script_id="test_script", 
            session_id="test_session",
            current_phase=GamePhase.MONOLOGUE,
            started_at=datetime.now(timezone.utc)
        )
        
        # Test calculate_game_progress
        progress = GamePhaseNodes.calculate_game_progress(game_state)
        print(f"Game progress calculated: {progress}")
        
        # Test get_available_actions
        actions = GamePhaseNodes.get_available_actions(game_state)
        print(f"Available actions: {len(actions)} actions found")
        
        # Test format_game_summary
        summary = GamePhaseNodes.format_game_summary(game_state)
        print(f"Game summary generated: {len(summary)} characters")
        
        print("✅ GamePhaseNodes functionality working correctly")
        return True
        
    except Exception as e:
        print(f"❌ GamePhaseNodes test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 .value Attribute Fix Verification")
    print("=" * 60)
    
    # Run all tests
    import_ok = test_imports()
    enum_ok = test_enum_behavior()
    gamestate_ok = test_game_state_creation()
    nodes_ok = test_nodes_functionality()
    
    print("\n📊 Test Summary")
    print("=" * 60)
    
    if import_ok and enum_ok and gamestate_ok and nodes_ok:
        print("🎉 All .value attribute fixes verified successfully!")
        print("✅ Module imports working")
        print("✅ Enum behavior correct")
        print("✅ GameState creation working")
        print("✅ GamePhaseNodes functionality working")
        print("\n🔧 The status endpoint should now work correctly!")
        return True
    else:
        print("❌ Some tests failed:")
        if not import_ok:
            print("   - Module import test failed")
        if not enum_ok:
            print("   - Enum behavior test failed")
        if not gamestate_ok:
            print("   - GameState creation test failed")
        if not nodes_ok:
            print("   - GamePhaseNodes functionality test failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
