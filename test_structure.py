#!/usr/bin/env python3
"""
Simple test to check that all modules can be imported correctly.
"""

def test_imports():
    """Test that all required modules can be imported."""
    
    # Test basic imports
    try:
        from config import TELEGRAM_BOT_TOKEN, OPENROUTER_API_KEY
        print("✓ config module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import config: {e}")
        
    try:
        from quest_engine import QuestEngine
        print("✓ quest_engine module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import quest_engine: {e}")
        
    try:
        from utils import detect_language
        print("✓ utils module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import utils: {e}")
        
    try:
        from telegram_bot import bot
        print("✓ telegram_bot module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import telegram_bot: {e}")

if __name__ == "__main__":
    test_imports()
    print("\nAll imports tested!")