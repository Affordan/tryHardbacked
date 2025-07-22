#!/usr/bin/env python3
"""
Script to update existing script data with complete character information.
"""

from app.database import SessionLocal, engine
from app.models.database_models import Base, Script

# 创建数据库会话
db = SessionLocal()

def update_script_characters():
    """Update script characters with complete information."""
    
    print("🔄 Updating script character data...")
    
    # 更新剧本1：午夜图书馆
    script1 = db.query(Script).filter(Script.id == "1").first()
    if script1:
        script1.characters = [
            {"name": "图书管理员", "avatar": "/placeholder.svg?height=60&width=60", "description": "知识渊博但性格孤僻的中年男性管理员，对图书馆的每一本书都了如指掌，但似乎隐藏着与失踪案相关的秘密"},
            {"name": "文学教授", "avatar": "/placeholder.svg?height=60&width=60", "description": "优雅的中年女教授，对古籍情有独钟，经常深夜来图书馆查阅资料，与失踪的管理员关系密切"},
            {"name": "神秘访客", "avatar": "/placeholder.svg?height=60&width=60", "description": "身份不明的年轻男子，似乎在寻找某本特殊的书籍，行为举止透露出不寻常的紧张感"},
            {"name": "夜班保安", "avatar": "/placeholder.svg?height=60&width=60", "description": "负责图书馆夜间安全的中年男性，性格谨慎，对图书馆的每个角落都很熟悉，可能目击了关键线索"},
            {"name": "研究生助理", "avatar": "/placeholder.svg?height=60&width=60", "description": "协助教授整理古籍的年轻女性，聪明敏锐，对图书馆的历史和传说有深入了解"},
            {"name": "古籍修复师", "avatar": "/placeholder.svg?height=60&width=60", "description": "专门修复珍贵古籍的年轻女性工匠，手艺精湛，经常与管理员合作，可能知道某些不为人知的秘密"}
        ]
        print("✅ Updated script 1: 午夜图书馆 (6 characters)")
    
    # 更新剧本2：雾都疑案
    script2 = db.query(Script).filter(Script.id == "2").first()
    if script2:
        script2.players = "6人 (3男3女)"
        script2.characters = [
            {"name": "首席探长", "avatar": "/placeholder.svg?height=60&width=60", "description": "经验丰富的苏格兰场老探长，直觉敏锐，办案手法独特，在伦敦警界享有盛誉"},
            {"name": "法医专家", "avatar": "/placeholder.svg?height=60&width=60", "description": "年轻的法医学专家，擅长尸体检验和现场分析，运用科学方法破解疑案，是探长的得力助手"},
            {"name": "神秘访客", "avatar": "/placeholder.svg?height=60&width=60", "description": "身份不明的神秘人物，似乎对案件有特殊了解，行为举止透露出不寻常的背景"},
            {"name": "贵族夫人", "avatar": "/placeholder.svg?height=60&width=60", "description": "维多利亚时代的上流社会贵族女性，优雅而聪慧，可能掌握着关键的社交圈信息"},
            {"name": "私家侦探", "avatar": "/placeholder.svg?height=60&width=60", "description": "独立工作的私人调查员，观察力敏锐，善于从细节中发现线索，与官方警察既合作又竞争"},
            {"name": "报社记者", "avatar": "/placeholder.svg?height=60&width=60", "description": "追踪案件真相的年轻女记者，消息灵通，敢于深入危险调查，可能掌握重要的内幕信息"}
        ]
        print("✅ Updated script 2: 雾都疑案 (6 characters)")
    
    # 提交更改
    db.commit()
    print("💾 Changes committed to database")

def verify_script_data():
    """Verify the updated script data."""
    
    print("\n🔍 Verifying script data...")
    
    # 验证剧本1
    script1 = db.query(Script).filter(Script.id == "1").first()
    if script1:
        print(f"📖 Script 1: {script1.title}")
        print(f"   Players: {script1.players}")
        print(f"   Characters: {len(script1.characters)}")
        for i, char in enumerate(script1.characters, 1):
            print(f"   {i}. {char['name']} - {char['description'][:50]}...")
    
    # 验证剧本2
    script2 = db.query(Script).filter(Script.id == "2").first()
    if script2:
        print(f"\n📖 Script 2: {script2.title}")
        print(f"   Players: {script2.players}")
        print(f"   Characters: {len(script2.characters)}")
        for i, char in enumerate(script2.characters, 1):
            print(f"   {i}. {char['name']} - {char['description'][:50]}...")

def test_character_matching():
    """Test if characters match the test script requirements."""
    
    print("\n🧪 Testing character matching with test scripts...")
    
    script2 = db.query(Script).filter(Script.id == "2").first()
    if script2:
        character_names = [char['name'] for char in script2.characters]
        
        # 检查测试脚本中使用的角色名称
        test_characters = ["法医专家", "神秘访客"]
        
        print(f"Available characters: {character_names}")
        print(f"Test script characters: {test_characters}")
        
        all_found = True
        for test_char in test_characters:
            if test_char in character_names:
                print(f"✅ Found: {test_char}")
            else:
                print(f"❌ Missing: {test_char}")
                all_found = False
        
        if all_found:
            print("🎉 All test characters are available in script 2!")
        else:
            print("⚠️  Some test characters are missing from script 2")
        
        return all_found
    
    return False

def main():
    """Main function to update and verify script data."""
    
    print("🚀 Script Data Update and Verification")
    print("=" * 50)
    
    try:
        # 更新脚本数据
        update_script_characters()
        
        # 验证数据
        verify_script_data()
        
        # 测试角色匹配
        character_match_success = test_character_matching()
        
        print("\n📊 Summary")
        print("=" * 50)
        
        if character_match_success:
            print("🎉 Script data update completed successfully!")
            print("✅ All characters are properly configured")
            print("✅ Test script compatibility verified")
        else:
            print("⚠️  Script data updated but some issues remain")
        
        return character_match_success
        
    except Exception as e:
        print(f"❌ Error updating script data: {e}")
        db.rollback()
        return False
    
    finally:
        db.close()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
