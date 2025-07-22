#!/usr/bin/env python3
"""
Debug script to test Dify API calls directly and identify the 400 Bad Request issue.
"""

import logging
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Configure logging to see debug output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from app.services.dify_service import call_qna_workflow, DifyServiceError

def test_dify_qna_call():
    """Test the Dify Q&A workflow call directly."""
    print("🔍 Testing Dify Q&A Workflow Call")
    print("=" * 50)

    # Test parameters
    char_id = "首席探长"
    act_num = 1
    query = "Hello, who are you?"
    history = "This is a test history context."
    model_name = "gpt-3.5-turbo"
    user_id = "debug_test_user"

    print(f"Parameters:")
    print(f"  char_id: {char_id}")
    print(f"  act_num: {act_num}")
    print(f"  query: {query}")
    print(f"  history: {history}")
    print(f"  model_name: {model_name}")
    print(f"  user_id: {user_id}")
    print()

    try:
        print("📞 Calling Dify Q&A workflow...")
        result = call_qna_workflow(
            char_id=char_id,
            act_num=act_num,
            query=query,
            history=history,
            model_name=model_name,
            user_id=user_id
        )

        print(f"✅ Success! Result: {result}")

    except DifyServiceError as e:
        print(f"❌ DifyServiceError: {e}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

def test_edge_cases():
    """Test edge cases that might cause 400 errors."""
    print("\n🧪 Testing Edge Cases")
    print("=" * 50)

    test_cases = [
        {
            "name": "Empty strings",
            "params": {
                "char_id": "",
                "act_num": 1,
                "query": "",
                "history": "",
                "model_name": "",
                "user_id": ""
            }
        },
        {
            "name": "None values",
            "params": {
                "char_id": "首席探长",
                "act_num": 1,
                "query": "Test",
                "history": None,
                "model_name": "gpt-3.5-turbo",
                "user_id": "test"
            }
        },
        {
            "name": "Invalid act_num type (string)",
            "params": {
                "char_id": "首席探长",
                "act_num": "1",  # String instead of int
                "query": "Test",
                "history": "Test history",
                "model_name": "gpt-3.5-turbo",
                "user_id": "test"
            }
        }
    ]

    for test_case in test_cases:
        print(f"\n🔬 Testing: {test_case['name']}")
        try:
            result = call_qna_workflow(**test_case['params'])
            print(f"✅ Success: {result[:100]}...")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_invalid_api_key():
    """Test with invalid API key to see 400 vs 401 error."""
    print("\n🔑 Testing Invalid API Key")
    print("=" * 50)

    # Temporarily modify the API key
    from app.core import config
    original_key = config.DIFY_QNA_WORKFLOW_API_KEY
    config.DIFY_QNA_WORKFLOW_API_KEY = "invalid-key"

    try:
        result = call_qna_workflow(
            char_id="首席探长",
            act_num=1,
            query="Test",
            history="Test history",
            model_name="gpt-3.5-turbo",
            user_id="test"
        )
        print(f"✅ Unexpected success: {result}")
    except Exception as e:
        print(f"❌ Expected error: {e}")
    finally:
        # Restore original key
        config.DIFY_QNA_WORKFLOW_API_KEY = original_key

if __name__ == "__main__":
    test_dify_qna_call()
    test_edge_cases()
    test_invalid_api_key()
