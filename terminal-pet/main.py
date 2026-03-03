#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TerminalPet - 终端电子宠物
在命令行里养宠物！
"""

import json
import os
import random
import time
from datetime import datetime, timedelta
from typing import Dict, Optional

# ============ 配置 ============

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
SAVE_FILE = os.path.join(DATA_DIR, 'save.json')

# 宠物类型定义
PET_TYPES = {
    'cat': {'name': '猫', 'emoji': '🐱', 'evolution': ['小猫', '成猫', '老猫']},
    'dog': {'name': '狗', 'emoji': '🐶', 'evolution': ['小狗', '成狗', '老狗']},
    'dragon': {'name': '龙', 'emoji': '🐲', 'evolution': ['幼龙', '成龙', '神龙']},
    'pixel': {'name': '像素怪', 'emoji': '👾', 'evolution': ['小怪', '大怪', '魔王']},
}

# ASCII 艺术
ASCII_ART = {
    'cat': [
        r'''
 /\_/\  
( >.<) 
(  "  ) 
 | | |  
/_| |_\\
''',
        r'''
 /\_/\  
( ^.^) 
(  "  ) 
 | | |  
/_| |_\\
''',
    ],
    'dog': [
        r'''
 __      __
/  \    /  \
|  |    |  |
|  |    |  |
 \  \  /  /
  \  \/  /
   \    /
    \  /
     \/
''',
    ],
    'dragon': [
        r'''
  __________
 /  _____  \
|  /     \  |
| |  O O  | |
| |   <   | |
|  \ _____/  |
 \_________/
''',
    ],
    'pixel': [
        r'''
 ┌───────┐
 │ ● _ ● │
 │  \_/  │
 └───────┘
''',
    ],
}


# ============ 宠物类 ============

class Pet:
    """电子宠物基类"""
    
    def __init__(self, name: str, pet_type: str = 'cat'):
        self.name = name
        self.pet_type = pet_type
        self.birth_time = datetime.now()
        self.last_interaction = datetime.now()
        
        # 状态值 (0-100)
        self.hunger = 50      # 饥饿 (越低越饿)
        self.happiness = 70   # 心情
        self.energy = 80      # 精力
        self.cleanliness = 90 # 清洁
        
        # 成长相关
        self.age_days = 0
        self.evolution_stage = 0  # 0=幼年，1=成年，2=老年
        self.exp = 0  # 经验值
        
        # 统计
        self.total_interactions = 0
        self.login_days = 1
        
        # 成就
        self.achievements = []
    
    def to_dict(self) -> Dict:
        """转换为字典（用于保存）"""
        return {
            'name': self.name,
            'pet_type': self.pet_type,
            'birth_time': self.birth_time.isoformat(),
            'last_interaction': self.last_interaction.isoformat(),
            'hunger': self.hunger,
            'happiness': self.happiness,
            'energy': self.energy,
            'cleanliness': self.cleanliness,
            'age_days': self.age_days,
            'evolution_stage': self.evolution_stage,
            'exp': self.exp,
            'total_interactions': self.total_interactions,
            'login_days': self.login_days,
            'achievements': self.achievements,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Pet':
        """从字典加载"""
        pet = cls(data['name'], data['pet_type'])
        pet.birth_time = datetime.fromisoformat(data['birth_time'])
        pet.last_interaction = datetime.fromisoformat(data['last_interaction'])
        pet.hunger = data['hunger']
        pet.happiness = data['happiness']
        pet.energy = data['energy']
        pet.cleanliness = data['cleanliness']
        pet.age_days = data['age_days']
        pet.evolution_stage = data['evolution_stage']
        pet.exp = data['exp']
        pet.total_interactions = data['total_interactions']
        pet.login_days = data['login_days']
        pet.achievements = data.get('achievements', [])
        return pet
    
    def update_states(self):
        """更新状态（随时间衰减）"""
        now = datetime.now()
        hours_passed = (now - self.last_interaction).total_seconds() / 3600
        
        # 状态衰减
        self.hunger = max(0, self.hunger - hours_passed * 5)
        self.happiness = max(0, self.happiness - hours_passed * 3)
        self.energy = max(0, self.energy - hours_passed * 4)
        self.cleanliness = max(0, self.cleanliness - hours_passed * 2)
        
        # 更新年龄
        days_passed = (now - self.birth_time).days
        self.age_days = days_passed
        
        # 更新进化阶段
        if self.age_days >= 30:
            self.evolution_stage = 2
        elif self.age_days >= 7:
            self.evolution_stage = 1
        else:
            self.evolution_stage = 0
        
        self.last_interaction = now
    
    def feed(self, amount: int = 20):
        """喂食"""
        self.hunger = min(100, self.hunger + amount)
        self.exp += 5
        self.total_interactions += 1
        return f"🍖 {self.name} 吃饱了！饥饿度 +{amount}"
    
    def play(self, duration: int = 30):
        """玩耍"""
        if self.energy < 20:
            return f"😴 {self.name} 太累了，不想玩..."
        
        self.happiness = min(100, self.happiness + duration)
        self.energy = max(0, self.energy - duration * 0.5)
        self.hunger = max(0, self.hunger - 10)
        self.exp += 10
        self.total_interactions += 1
        return f"🎾 {self.name} 玩得很开心！心情 +{duration}"
    
    def sleep(self):
        """睡觉"""
        self.energy = 100
        self.hunger = max(0, self.hunger - 10)
        self.total_interactions += 1
        return f"💤 {self.name} 睡了一觉，精力恢复了！"
    
    def clean(self):
        """清洁"""
        self.cleanliness = 100
        self.happiness = min(100, self.happiness + 5)
        self.total_interactions += 1
        return f"🛁 {self.name} 变干净了！"
    
    def check_achievements(self):
        """检查成就"""
        new_achievements = []
        
        if self.login_days >= 3 and '新手训练师' not in self.achievements:
            new_achievements.append('新手训练师')
        
        if self.evolution_stage >= 1 and '超级奶爸' not in self.achievements:
            new_achievements.append('超级奶爸')
        
        if self.evolution_stage >= 2 and '进化大师' not in self.achievements:
            new_achievements.append('进化大师')
        
        self.achievements.extend(new_achievements)
        return new_achievements
    
    def get_status_display(self) -> str:
        """获取状态显示"""
        pet_info = PET_TYPES.get(self.pet_type, PET_TYPES['cat'])
        evolution_name = pet_info['evolution'][self.evolution_stage]
        
        def get_bar(value: int, max_value: int = 100) -> str:
            filled = int(value / max_value * 10)
            empty = 10 - filled
            return '█' * filled + '░' * empty
        
        status = f"""
╭─────────────────────────────╮
│     🐾 {self.name} - {evolution_name}     │
╰─────────────────────────────╯

{pet_info['emoji']} 宠物类型：{pet_info['name']}
📅 年龄：{self.age_days} 天
⭐ 经验：{self.exp}

━━━━━━━━━━━━━━━━━━━━━
❤️  心情：[{get_bar(self.happiness)}] {int(self.happiness)}/100
🍖  饥饿：[{get_bar(self.hunger)}] {int(self.hunger)}/100
⚡  精力：[{get_bar(self.energy)}] {int(self.energy)}/100
✨  清洁：[{get_bar(self.cleanliness)}] {int(self.cleanliness)}/100
━━━━━━━━━━━━━━━━━━━━━

🏆 成就：{', '.join(self.achievements) if self.achievements else '暂无'}
🎮 互动次数：{self.total_interactions}
"""
        return status
    
    def get_ascii_art(self) -> str:
        """获取 ASCII 艺术"""
        arts = ASCII_ART.get(self.pet_type, ASCII_ART['cat'])
        # 根据心情选择表情
        if self.happiness >= 70:
            return arts[0] if len(arts) > 0 else arts[0]
        else:
            return arts[-1] if len(arts) > 1 else arts[0]


# ============ 存档管理 ============

class SaveManager:
    """存档管理器"""
    
    @staticmethod
    def save(pet: Pet):
        """保存宠物数据"""
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(pet.to_dict(), f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def load() -> Optional[Pet]:
        """加载宠物数据"""
        if not os.path.exists(SAVE_FILE):
            return None
        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Pet.from_dict(data)
        except Exception as e:
            print(f"加载存档失败：{e}")
            return None
    
    @staticmethod
    def delete():
        """删除存档"""
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)


# ============ 主游戏类 ============

class Game:
    """游戏主类"""
    
    def __init__(self):
        self.pet: Optional[Pet] = None
        self.running = True
    
    def start(self):
        """开始游戏"""
        print("\n" + "=" * 40)
        print("     🐾 TerminalPet v0.1 🐾")
        print("=" * 40)
        
        # 尝试加载存档
        self.pet = SaveManager.load()
        
        if self.pet:
            print(f"\n✅ 读取存档成功！欢迎回来，{self.pet.name}！")
            self.pet.update_states()
            self.pet.login_days += 1
        else:
            self.create_pet()
        
        # 主循环
        self.main_loop()
    
    def create_pet(self):
        """创建新宠物"""
        print("\n🎉 欢迎来到 TerminalPet！")
        print("请选择你的宠物：")
        print("1. 🐱 猫")
        print("2. 🐶 狗")
        print("3. 🐲 龙")
        print("4. 👾 像素怪")
        
        while True:
            choice = input("\n请选择 (1-4): ").strip()
            pet_map = {'1': 'cat', '2': 'dog', '3': 'dragon', '4': 'pixel'}
            if choice in pet_map:
                pet_type = pet_map[choice]
                break
            print("无效选择，请重新输入！")
        
        name = input("给你的宠物起个名字：").strip() or "小咪"
        self.pet = Pet(name, pet_type)
        
        print(f"\n✨ {self.pet.name} 加入了你的家庭！")
        print(self.pet.get_ascii_art())
    
    def main_loop(self):
        """主游戏循环"""
        while self.running:
            self.show_menu()
            try:
                choice = input("\n请选择命令 (1-6): ").strip()
            except EOFError:
                print("\n\n👋 检测到输入结束，游戏已保存！")
                self.quit_game()
                break
            self.handle_command(choice)
    
    def show_menu(self):
        """显示菜单"""
        print(self.pet.get_status_display())
        print("╭─────────────────────────────╮")
        print("│  [1] 喂食    [2] 玩耍       │")
        print("│  [3] 睡觉    [4] 清洁       │")
        print("│  [5] 状态    [6] 退出       │")
        print("╰─────────────────────────────╯")
    
    def handle_command(self, choice: str):
        """处理命令"""
        if choice == '1':
            print(self.pet.feed())
        elif choice == '2':
            print(self.pet.play())
        elif choice == '3':
            print(self.pet.sleep())
        elif choice == '4':
            print(self.pet.clean())
        elif choice == '5':
            print(self.pet.get_status_display())
        elif choice == '6':
            self.quit_game()
        else:
            print("❌ 无效命令！")
        
        # 检查成就
        new_achievements = self.pet.check_achievements()
        if new_achievements:
            print(f"\n🏆 解锁新成就：{', '.join(new_achievements)}！")
        
        # 自动保存
        SaveManager.save(self.pet)
        input("\n按回车继续...")
    
    def quit_game(self):
        """退出游戏"""
        SaveManager.save(self.pet)
        print(f"\n💾 游戏已保存！{self.pet.name} 期待下次见面！")
        print(self.pet.get_ascii_art())
        self.running = False


# ============ 入口 ============

if __name__ == '__main__':
    try:
        game = Game()
        game.start()
    except KeyboardInterrupt:
        print("\n\n👋 游戏已退出！")
    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
        import traceback
        traceback.print_exc()
