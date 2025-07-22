#!/usr/bin/env python3
"""
Verification script to check if history parameter injection fix is correctly implemented.
"""

import sys
import os

def check_dify_service():
    """Check if dify_service.py has correct function signature."""
    print("🔍 Checking dify_service.py...")
    
    try:
        with open('app/services/dify_service.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check function signature
        if 'def call_qna_workflow(' in content:
            # Find the function definition
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'def call_qna_workflow(' in line:
                    # Get the function signature (next few lines)
                    signature_lines = []
                    j = i
                    while j < len(lines) and not lines[j].strip().endswith(') -> str:'):
                        signature_lines.append(lines[j].strip())
                        j += 1
                    if j < len(lines):
                        signature_lines.append(lines[j].strip())
                    
                    signature = ' '.join(signature_lines)
                    print(f"   Found signature: {signature}")
                    
                    # Check if history parameter is in correct position
                    if 'history: Optional[str]' in signature:
                        print("   ✅ history parameter found")
                        
                        # Check parameter order
                        if 'query: str, history: Optional[str], model_name: str' in signature:
                            print("   ✅ Parameter order is correct")
                        else:
                            print("   ❌ Parameter order may be incorrect")
                            return False
                    else:
                        print("   ❌ history parameter not found")
                        return False
                    break
        
        # Check inputs dictionary
        if '"history": history or "没有历史记录。"' in content:
            print("   ✅ history field added to inputs dictionary")
        else:
            print("   ❌ history field not found in inputs dictionary")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error checking dify_service.py: {e}")
        return False

def check_dify_tools():
    """Check if dify_tools.py has correct function signature."""
    print("\n🔍 Checking dify_tools.py...")
    
    try:
        with open('app/langchain/tools/dify_tools.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check _run method signature
        if 'def _run(' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'def _run(' in line and 'DifyQnATool' in content[max(0, content.rfind('class', 0, content.find(line))):content.find(line)]:
                    # Get the method signature
                    signature_lines = []
                    j = i
                    while j < len(lines) and not lines[j].strip().endswith(') -> str:'):
                        signature_lines.append(lines[j].strip())
                        j += 1
                    if j < len(lines):
                        signature_lines.append(lines[j].strip())
                    
                    signature = ' '.join(signature_lines)
                    print(f"   Found _run signature: {signature}")
                    
                    # Check if history parameter exists
                    if 'history: Optional[str] = None' in signature:
                        print("   ✅ history parameter found in _run method")
                    else:
                        print("   ❌ history parameter not found in _run method")
                        return False
                    break
        
        # Check call_qna_workflow call
        if 'history=history,' in content:
            print("   ✅ history parameter passed to call_qna_workflow")
        else:
            print("   ❌ history parameter not passed to call_qna_workflow")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error checking dify_tools.py: {e}")
        return False

def check_game_engine():
    """Check if game_engine.py correctly passes history context."""
    print("\n🔍 Checking game_engine.py...")
    
    try:
        with open('app/langchain/engine/game_engine.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if _format_history_for_prompt method exists
        if 'def _format_history_for_prompt(' in content:
            print("   ✅ _format_history_for_prompt method found")
        else:
            print("   ❌ _format_history_for_prompt method not found")
            return False
        
        # Check if history_context is generated
        if 'history_context = self._format_history_for_prompt(game_state)' in content:
            print("   ✅ history_context generation found")
        else:
            print("   ❌ history_context generation not found")
            return False
        
        # Check if history is passed to qna_tool._run
        if 'history=history_context' in content:
            print("   ✅ history_context passed to qna_tool._run")
        else:
            print("   ❌ history_context not passed to qna_tool._run")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error checking game_engine.py: {e}")
        return False

def main():
    """Main verification function."""
    print("🔧 History Parameter Injection Fix Verification")
    print("=" * 60)
    
    # Check all three files
    dify_service_ok = check_dify_service()
    dify_tools_ok = check_dify_tools()
    game_engine_ok = check_game_engine()
    
    print("\n📊 Verification Summary")
    print("=" * 60)
    
    if dify_service_ok and dify_tools_ok and game_engine_ok:
        print("🎉 All history parameter injection fixes verified!")
        print("✅ dify_service.py: Function signature and inputs correct")
        print("✅ dify_tools.py: Parameter passing correct")
        print("✅ game_engine.py: History context generation and injection correct")
        print("\n🚀 The fix should resolve the missing history parameter issue!")
        print("📋 Expected outcome:")
        print("   - Dify workflow logs should now show both 'query' and 'history' parameters")
        print("   - Q&A responses will be contextually aware of previous events")
        print("   - Frontend API calls remain unchanged")
        return True
    else:
        print("❌ Some verification checks failed:")
        if not dify_service_ok:
            print("   - dify_service.py issues detected")
        if not dify_tools_ok:
            print("   - dify_tools.py issues detected")
        if not game_engine_ok:
            print("   - game_engine.py issues detected")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
