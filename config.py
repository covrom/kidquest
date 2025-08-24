import os

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# OpenRouter API Configuration  
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Model configuration
MODEL_NAME = "qwen/qwen3-4b:free"

# Bot settings
BOT_NAME = "KidQuestBot"
MAX_OPTIONS_PER_STEP = 3