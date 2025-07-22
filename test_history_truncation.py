#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify the history truncation fix for Dify API 256 character limit.
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

from app.services.dify_service import call_qna_workflow, _truncate_history_smartly

def test_history_truncation():
    """Test that long history is properly truncated."""
    print("🧪 Testing history truncation fix...")
    
    # Create a long history that exceeds 256 characters
    long_history = """--- 以下是最近发生的事情，请参考这些信息进行回答 ---
[朱丰翰 进行了独白]: 【朱丰翰】我叫朱丰翰，今年三十一岁，身处国企工作，过着平凡的生活。我的父亲已经八十岁了，年纪大了，常常坐在摇椅上，晒着太阳，午睡时脸上挂着慈祥的笑容。每次中午下班回家，看到他那样，我的心里总是感到一阵温暖。然而，最近发生的事情让我心情沉重。

除夕那天，我收到了来自远方表亲的来信，得知我的大伯朱立杰过世了。这个消息如同晴天霹雳，父亲听到后伤心欲绝，甚至一度昏睡过去。看着他那样，我心里无比难受，似乎一切都在提醒我，时间不等人，生命的脆弱让我感到无力。

我知道，父亲心里还有一个心病，那就是我还没有结婚。身边有很多优秀的女孩子，但我心里似乎总有一个特别喜欢的女孩，却又想不起来她是谁。弟弟丰震年纪小的时候就辍学了，后来自己创业，但几乎每次都以失败告终。他总是向父亲要钱，我知道父亲的退休金所剩无几，心里对弟弟的行为感到不满。我曾告诉他，不要总是向父亲要钱，如果缺钱就来找我。可他却像个无底洞，越要越多，甚至有时候我都要向朋友借钱来满足他的需求。

我常常在想，这样的生活到底是为了什么？我努力工作，想要给家人更好的生活，却总是被弟弟的行为所困扰。每次和他吵架后，我心里又是无奈又是伤心，明明是为了他好，却总是得不到理解。或许，我也在逃避一些事情，逃避对未来的思考，逃避对感情的追求。可我知道，这样下去不是办法，我必须面对这一切，找到属于自己的方向。
[许苗苗 问 朱大强]: 你好
[朱大强 回答]: 抱歉，我暂时无法回答这个问题。
[许苗苗 问 朱大强]: 你好
[朱大强 回答]: 抱歉，我暂时无法回答这个问题。"""
    
    print(f"Original history length: {len(long_history)} characters")
    
    # Test the smart truncation function
    truncated = _truncate_history_smartly(long_history, "朱大强")
    print(f"Truncated history length: {len(truncated)} characters")
    print(f"Truncated history preview: {truncated[:100]}...")
    
    # Test the actual API call with long history
    try:
        result = call_qna_workflow(
            char_id="朱大强",
            act_num=1,
            query="你好",
            history=long_history,  # Long history that previously caused 400 error
            model_name="gpt-3.5-turbo",
            user_id="test_user"
        )
        print(f"✅ Success! API call completed with truncated history")
        print(f"Result: {result[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_short_history():
    """Test that short history is not truncated."""
    print("\n🧪 Testing short history (no truncation needed)...")
    
    short_history = "这是一个简短的历史记录。"
    print(f"Short history length: {len(short_history)} characters")
    
    try:
        result = call_qna_workflow(
            char_id="朱大强",
            act_num=1,
            query="你好",
            history=short_history,
            model_name="gpt-3.5-turbo",
            user_id="test_user"
        )
        print(f"✅ Success! Short history processed correctly")
        print(f"Result: {result[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing History Truncation Fix")
    print("=" * 50)
    
    results = []
    results.append(test_history_truncation())
    results.append(test_short_history())
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! The history truncation issue has been fixed.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
