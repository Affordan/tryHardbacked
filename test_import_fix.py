#!/usr/bin/env python3
"""
Test script to verify that the history parameter fix doesn't break imports.
"""

def test_imports():
    """Test that all modules can be imported after the fix."""
    print("🔍 Testing imports after history parameter fix...")
    
    try:
        print("   Testing dify_service import...")
        from app.services.dify_service import call_qna_workflow
        print("   ✅ dify_service imported successfully")
        
        print("   Testing dify_tools import...")
        from app.langchain.tools.dify_tools import DifyQnATool
        print("   ✅ dify_tools imported successfully")
        
        print("   Testing game_engine import...")
        from app.langchain.engine.game_engine import GameEngine
        print("   ✅ game_engine imported successfully")
        
        print("   Testing main app import...")
        from app.main import app
        print("   ✅ main app imported successfully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

def test_function_signatures():
    """Test that function signatures are correct."""
    print("\n🔍 Testing function signatures...")
    
    try:
        from app.services.dify_service import call_qna_workflow
        import inspect
        
        # Get function signature
        sig = inspect.signature(call_qna_workflow)
        params = list(sig.parameters.keys())
        
        print(f"   call_qna_workflow parameters: {params}")
        
        # Check expected parameter order
        expected_order = ['char_id', 'act_num', 'query', 'history', 'model_name', 'user_id']
        if params == expected_order:
            print("   ✅ Parameter order is correct")
            return True
        else:
            print(f"   ❌ Parameter order incorrect. Expected: {expected_order}, Got: {params}")
            return False
        
    except Exception as e:
        print(f"   ❌ Signature test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 History Parameter Fix Import Test")
    print("=" * 50)
    
    import_ok = test_imports()
    signature_ok = test_function_signatures()
    
    print("\n📊 Test Summary")
    print("=" * 50)
    
    if import_ok and signature_ok:
        print("🎉 All tests passed!")
        print("✅ Imports working correctly")
        print("✅ Function signatures correct")
        print("✅ History parameter fix is ready for testing")
        return True
    else:
        print("❌ Some tests failed:")
        if not import_ok:
            print("   - Import test failed")
        if not signature_ok:
            print("   - Signature test failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
