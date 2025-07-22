#!/usr/bin/env python3
"""
Test script to verify the Pydantic v2.11.7 compatibility fix for Dify tools.

This script tests the DifyMonologueTool and DifyQnATool classes to ensure
they can be instantiated correctly after the args_schema field annotation fix.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_dify_tools_import():
    """Test that Dify tools can be imported without errors."""
    try:
        from app.langchain.tools.dify_tools import DifyMonologueTool, DifyQnATool, create_dify_tools
        print("✅ Successfully imported Dify tools")
        return True
    except Exception as e:
        print(f"❌ Failed to import Dify tools: {e}")
        return False

def test_tool_instantiation():
    """Test that tools can be instantiated correctly."""
    try:
        from app.langchain.tools.dify_tools import DifyMonologueTool, DifyQnATool
        
        # Test DifyMonologueTool instantiation
        monologue_tool = DifyMonologueTool()
        print(f"✅ DifyMonologueTool instantiated successfully")
        print(f"   - Name: {monologue_tool.name}")
        print(f"   - Description: {monologue_tool.description[:50]}...")
        print(f"   - Args schema: {monologue_tool.args_schema}")
        
        # Test DifyQnATool instantiation
        qna_tool = DifyQnATool()
        print(f"✅ DifyQnATool instantiated successfully")
        print(f"   - Name: {qna_tool.name}")
        print(f"   - Description: {qna_tool.description[:50]}...")
        print(f"   - Args schema: {qna_tool.args_schema}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to instantiate tools: {e}")
        return False

def test_create_tools_function():
    """Test the create_dify_tools function."""
    try:
        from app.langchain.tools.dify_tools import create_dify_tools
        
        tools = create_dify_tools()
        print(f"✅ create_dify_tools() returned {len(tools)} tools")
        
        for i, tool in enumerate(tools):
            print(f"   Tool {i+1}: {tool.name} - {type(tool).__name__}")
            
        return True
    except Exception as e:
        print(f"❌ Failed to create tools: {e}")
        return False

def test_pydantic_validation():
    """Test that Pydantic validation works correctly."""
    try:
        from app.langchain.tools.dify_tools import MonologueInput, QnAInput
        
        # Test MonologueInput validation
        monologue_input = MonologueInput(
            char_id="test_character",
            act_num=1,
            model_name="gpt-3.5-turbo",
            user_id="test_user"
        )
        print("✅ MonologueInput validation works")
        
        # Test QnAInput validation
        qna_input = QnAInput(
            char_id="test_character",
            act_num=1,
            query="Who are you?",
            model_name="gpt-3.5-turbo",
            user_id="test_user"
        )
        print("✅ QnAInput validation works")
        
        return True
    except Exception as e:
        print(f"❌ Pydantic validation failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Dify Tools Pydantic v2.11.7 Compatibility Fix")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_dify_tools_import),
        ("Tool Instantiation Test", test_tool_instantiation),
        ("Create Tools Function Test", test_create_tools_function),
        ("Pydantic Validation Test", test_pydantic_validation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"   Test failed!")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Pydantic v2.11.7 fix is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    exit(main())
