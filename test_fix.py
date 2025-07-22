#!/usr/bin/env python3
"""
Test script to verify the 400 Bad Request fix.
"""

import logging
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from app.services.dify_service import call_qna_workflow

def test_empty_user_id_fix():
    """Test that empty user_id no longer causes 400 errors."""
    print("🧪 Testing fix for empty user_id...")
    
    try:
        result = call_qna_workflow(
            char_id="首席探长",
            act_num=1,
            query="Test question",
            history="Test history",
            model_name="gpt-3.5-turbo",
            user_id=""  # Empty user_id that previously caused 400 error
        )
        print(f"✅ Success! Result: {result[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_none_user_id_fix():
    """Test that None user_id is handled properly."""
    print("\n🧪 Testing fix for None user_id...")
    
    try:
        result = call_qna_workflow(
            char_id="首席探长",
            act_num=1,
            query="Test question",
            history="Test history",
            model_name="gpt-3.5-turbo",
            user_id=None  # None user_id
        )
        print(f"✅ Success! Result: {result[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_whitespace_user_id_fix():
    """Test that whitespace-only user_id is handled properly."""
    print("\n🧪 Testing fix for whitespace-only user_id...")
    
    try:
        result = call_qna_workflow(
            char_id="首席探长",
            act_num=1,
            query="Test question",
            history="Test history",
            model_name="gpt-3.5-turbo",
            user_id="   "  # Whitespace-only user_id
        )
        print(f"✅ Success! Result: {result[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing 400 Bad Request Fixes")
    print("=" * 50)
    
    results = []
    results.append(test_empty_user_id_fix())
    results.append(test_none_user_id_fix())
    results.append(test_whitespace_user_id_fix())
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! The 400 Bad Request issue has been fixed.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
