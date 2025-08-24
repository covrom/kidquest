#!/usr/bin/env python3
"""
KidQuest Telegram Bot - Main Entry Point
"""

import asyncio
import logging
from telegram_bot import bot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    """Start the bot."""
    print("Starting KidQuestBot...")
    try:
        # Run the bot
        bot.run()
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Error starting bot: {e}")

if __name__ == '__main__':
    main()