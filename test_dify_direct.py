#!/usr/bin/env python3
"""
Direct test of dify_service to isolate the 400 error issue.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

def test_dify_service_direct():
    """Test dify_service directly to isolate issues."""
    print("🔍 Testing dify_service directly...")
    
    try:
        from app.services.dify_service import call_qna_workflow
        
        # Test parameters
        char_id = "首席探长"
        act_num = 1
        query = "你好，请介绍一下你自己。"
        history = "--- 以下是最近发生的事情，请参考这些信息进行回答 ---\n[首席探长 进行了独白]: 我是一名首席探长，名叫李明。"
        model_name = "qwen"
        user_id = "test_user"
        
        print(f"   char_id: {char_id}")
        print(f"   act_num: {act_num}")
        print(f"   query: {query}")
        print(f"   history length: {len(history)}")
        print(f"   model_name: {model_name}")
        print(f"   user_id: {user_id}")
        
        # Call the function
        print("\n📤 Calling call_qna_workflow...")
        answer = call_qna_workflow(
            char_id=char_id,
            act_num=act_num,
            query=query,
            history=history,
            model_name=model_name,
            user_id=user_id
        )
        
        print(f"📥 Answer received: {answer}")
        
        # Check if we got the fallback error message
        if "抱歉，我暂时无法回答这个问题" in answer:
            print("❌ Received fallback error message - Dify API call failed")
            return False
        else:
            print("✅ Received proper AI response - Dify API working correctly")
            return True
        
    except Exception as e:
        print(f"❌ Error testing dify_service: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dify_tools_direct():
    """Test DifyQnATool directly."""
    print("\n🔍 Testing DifyQnATool directly...")
    
    try:
        from app.langchain.tools.dify_tools import DifyQnATool
        
        # Create tool instance
        tool = DifyQnATool()
        
        # Test parameters
        char_id = "首席探长"
        act_num = 1
        query = "你好，请介绍一下你自己。"
        history = "--- 以下是最近发生的事情，请参考这些信息进行回答 ---\n[首席探长 进行了独白]: 我是一名首席探长，名叫李明。"
        model_name = "qwen"
        user_id = "test_user"
        
        print(f"   Testing with history length: {len(history)}")
        
        # Call the tool
        print("\n📤 Calling DifyQnATool._run...")
        answer = tool._run(
            char_id=char_id,
            act_num=act_num,
            query=query,
            model_name=model_name,
            user_id=user_id,
            history=history
        )
        
        print(f"📥 Answer received: {answer}")
        
        # Check if we got the fallback error message
        if "抱歉，我暂时无法回答这个问题" in answer:
            print("❌ Received fallback error message - Tool call failed")
            return False
        else:
            print("✅ Received proper AI response - Tool working correctly")
            return True
        
    except Exception as e:
        print(f"❌ Error testing DifyQnATool: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🧪 Direct Dify Service Test")
    print("=" * 50)
    
    # Test 1: Direct dify_service call
    service_ok = test_dify_service_direct()
    
    # Test 2: Direct DifyQnATool call
    tool_ok = test_dify_tools_direct()
    
    print("\n📊 Test Summary")
    print("=" * 50)
    
    if service_ok and tool_ok:
        print("🎉 All direct tests passed!")
        print("✅ dify_service working correctly")
        print("✅ DifyQnATool working correctly")
        return True
    else:
        print("❌ Some direct tests failed:")
        if not service_ok:
            print("   - dify_service test failed")
        if not tool_ok:
            print("   - DifyQnATool test failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
