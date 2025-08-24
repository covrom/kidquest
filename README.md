# KidQuest Telegram Bot

Telegram bot that creates interactive text-based quests for children (ages 5-7).

## Features

- Create custom quests based on user requirements
- Generate quest scenarios using AI (OpenRouter + qwen/qwen3-4b:free model)
- Interactive storytelling with multiple choices and endings
- Dynamic branching when user makes unexpected choices
- Simple, child-friendly language
- Positive, educational content

## Requirements

- Python 3.7+
- Telegram Bot Token (set as TELEGRAM_BOT_TOKEN environment variable)
- OpenRouter API Key (set as OPENROUTER_API_KEY environment variable)

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install python-telegram-bot openai
   ```

## Configuration

Set these environment variables:

```bash
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token_here"
export OPENROUTER_API_KEY="your_openrouter_api_key_here"
```

## Usage

1. Start the bot with: `python main.py`
2. Send `/new` to start a new quest
3. Provide requirements for your quest (topic, characters, educational elements)
4. Follow the interactive story and make choices!

## Project Structure

- `main.py` - Main entry point
- `config.py` - Configuration settings  
- `telegram_bot.py` - Telegram bot logic with command handlers
- `quest_engine.py` - Quest generation and execution engine
- `utils.py` - Utility functions (language detection, etc.)

## How It Works

1. User sends `/new` to start a new quest
2. Bot asks for requirements description 
3. User provides free-text description of desired quest
4. Bot generates JSON quest scenario using AI
5. Quest execution begins from the first step
6. For each step, bot displays text and options with emojis
7. User makes choice (free text)
8. Bot matches user's choice to available options using LLM
9. If no match found, creates new branch via LLM
10. Story continues until ending is reached

## License

MIT
