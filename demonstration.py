#!/usr/bin/env python3
"""
Demonstration of how KidQuest Telegram Bot works.
This shows the core functionality without requiring external API calls.
"""

import json
from quest_engine import QuestEngine

async def demonstrate_quest_generation():
    """Demonstrate quest generation with sample requirements."""
    
    print("=== KidQuest Bot Demonstration ===\n")
    
    # Create a quest engine instance
    engine = QuestEngine()
    
    # Sample user requirements
    requirements = (
        "Тема: приключения в лесу. "
        "Главный герой: маленький дракон по имени Драко. "
        "Образовательный элемент: изучение животных и растений. "
        "Количество шагов: 5"
    )
    
    print("User requirements:")
    print(requirements)
    print("\n" + "="*50 + "\n")
    
    # Generate quest
    print("Generating quest...")
    quest_data = await engine.generate_quest(requirements)
    
    if quest_data:
        print("✅ Quest generated successfully!")
        
        # Display basic information about the quest
        quest_info = quest_data['quest']
        print(f"Title: {quest_info['title']}")
        print(f"Start Step ID: {quest_info['startStepId']}")
        print(f"Total Steps: {len(quest_info['steps'])}")
        
        # Show first few steps
        print("\nFirst 2 steps:")
        for i, step in enumerate(quest_info['steps'][:2]):
            print(f"\nStep {i+1} (ID: {step['id']}):")
            print(f"  Text: {step['text'][:80]}...")
            if step['options']:
                print("  Options:")
                for option in step['options']:
                    print(f"    - {option['emoji']} {option['text']}")
        
        # Show ending steps
        print("\nEnding steps:")
        ending_steps = [s for s in quest_info['steps'] if len(s['options']) == 0]
        for i, step in enumerate(ending_steps):
            print(f"\nEnding {i+1} (ID: {step['id']}):")
            print(f"  Text: {step['text'][:80]}...")
            
    else:
        print("❌ Failed to generate quest")

async def demonstrate_choice_processing():
    """Demonstrate choice processing."""
    
    print("\n" + "="*50)
    print("Choice Processing Demonstration")
    print("="*50)
    
    engine = QuestEngine()
    
    # Sample step and user choice
    sample_step = {
        "id": "step_1",
        "text": "Ты видишь красивую птицу в небе. Что ты хочешь сделать?",
        "options": [
            {
                "text": "Попробовать поймать её", 
                "nextStepId": "step_2a",
                "emoji": "🕊️"
            },
            {
                "text": "Подождать и наблюдать", 
                "nextStepId": "step_2b",
                "emoji": "👀"  
            }
        ]
    }
    
    user_choice = "попробовать поймать"
    
    print(f"Current step text: {sample_step['text']}")
    print(f"User choice: {user_choice}")
    
    # Process the choice
    next_step_id = await engine.process_choice(sample_step, user_choice, [sample_step])
    
    if next_step_id:
        print(f"✅ Matched to next step ID: {next_step_id}")
    else:
        print("❌ No matching option found - would create new branch")

async def demonstrate_branch_creation():
    """Demonstrate dynamic branching."""
    
    print("\n" + "="*50)
    print("Dynamic Branch Creation Demonstration")
    print("="*50)
    
    engine = QuestEngine()
    
    # Sample current step
    sample_step = {
        "id": "step_2b",
        "text": "Ты внимательно наблюдаешь за птицей и видишь, как она делает красивые манёвры!",
        "options": [
            {
                "text": "Попробовать повторить движения", 
                "nextStepId": "ending_1",
                "emoji": "🦘"
            },
            {
                "text": "Сделать рисунок птицы",
                "nextStepId": "ending_3",
                "emoji": "✏️"  
            }
        ]
    }
    
    user_choice = "я хочу сделать сюрприз для птицы"
    
    print(f"Current step text: {sample_step['text']}")
    print(f"User choice: {user_choice}")
    
    # Try to create a new branch
    new_branch = await engine.create_new_branch(sample_step, user_choice, [sample_step])
    
    if new_branch:
        print("✅ New branch created successfully!")
        print(f"New step ID: {new_branch['id']}")
        print(f"New step text: {new_branch['text'][:60]}...")
        if new_branch['options']:
            print("New options:")
            for option in new_branch['options']:
                print(f"  - {option['emoji']} {option['text']}")
    else:
        print("❌ Failed to create new branch")

if __name__ == "__main__":
    import asyncio
    
    print("KidQuest Bot Demonstration")
    print("This shows how the system would work with real data\n")
    
    # Run all demonstrations
    asyncio.run(demonstrate_quest_generation())
    asyncio.run(demonstrate_choice_processing()) 
    asyncio.run(demonstrate_branch_creation())
    
    print("\n" + "="*50)
    print("Demonstration Complete!")
    print("="*50)
    print("\nThe system is ready to be integrated with:")
    print("- Telegram Bot framework")
    print("- OpenRouter API for LLM calls") 
    print("- Real-time user interaction")