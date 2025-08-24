# KidQuest Telegram Bot - System Architecture

## Overview
This is a Python-based Telegram bot that creates interactive text-based quests for children (ages 5-7). The bot allows users to initiate new quests with specific requirements, generates quest scenarios using AI, and provides an engaging storytelling experience.

## Core Components

### 1. Telegram Bot Framework
- Uses python-telegram-bot library 
- Handles /new command to start new quests
- Manages user state during quest execution
- Processes user text input for choices

### 2. Quest Generation Engine
- Integrates with OpenRouter/OpenAI API using qwen/qwen3-4b:free model
- Takes user requirements description as input
- Generates JSON quest scenarios following specified format
- Ensures educational elements, simple language, and positive endings

### 3. Quest Execution Engine  
- Manages quest state (current step, history)
- Displays scenario text with emoji options
- Processes user choices using LLM matching
- Handles dynamic branching when needed

### 4. Language Processing
- Detects user's input language 
- Generates all quest content in the same language
- Ensures simple, child-friendly vocabulary

## Data Structures

### Quest JSON Format
```json
{
  "quest": {
    "title": "название квеста",
    "startStepId": "id начального шага",
    "steps": [
      {
        "id": "уникальный идентификатор шага",
        "image": "описание картинки для визуализации",
        "text": "текст сценария",
        "options": [
          {
            "text": "текст выбора",
            "nextStepId": "id следующего шага", 
            "emoji": "визуальная подсказка"
          }
        ]
      }
    ]
  }
}
```

### User Session State
```python
{
    "user_id": int,
    "current_quest": QuestObject,  # The active quest
    "current_step_id": str,         # Current step in the quest  
    "step_history": [str],          # History of visited steps (for backtracking)
    "quest_started": bool         # Whether quest has started
}
```

## Workflow

### 1. Quest Initiation
- User sends `/new` command
- Bot requests requirements description 
- User provides free-text description with topic, characters, etc.
- Bot generates JSON scenario using LLM

### 2. Quest Execution  
- Start from initial step
- Display text and options (with emojis)
- Wait for user choice (free text)

### 3. Choice Processing
- Match user's text to available options using LLM
- If match found, proceed to next step
- If no match, create new branch via LLM

### 4. Dynamic Branching
- When no suitable option is found:
  - Generate new branching scenario 
  - Add new steps to quest structure
  - Continue story flow

## Technical Requirements

### API Integration
- OpenRouter with qwen/qwen3-4b:free model
- RESTful API calls for LLM interactions
- Error handling for API failures

### Language Support  
- Automatic language detection from user input
- All generated content in detected language
- Simple vocabulary appropriate for 5-7 year olds

### Design Constraints
- Each step has max 2-3 choices
- Include emojis for visual cues
- Positive, good-hearted storylines
- Educational elements included
- Converging to multiple endings

## Implementation Plan (in code mode)

1. Create project structure and dependencies
2. Implement Telegram bot framework with /new command handling  
3. Design quest scenario generation using OpenAI API through OpenRouter
4. Implement quest state management 
5. Create quest execution logic with step-by-step display
6. Implement user choice processing and LLM-based option matching
7. Add dynamic branching capability when no suitable option is found
8. Implement language detection and localization
9. Test the complete workflow
10. Document implementation

## File Structure
```
kidquest/
├── main.py                 # Main bot entry point
├── config.py               # Configuration settings  
├── telegram_bot.py         # Telegram bot logic
├── quest_generator.py      # LLM-based quest generation
├── quest_engine.py         # Quest execution and state management
├── utils.py                # Utility functions (language detection, etc.)
└── requirements.txt        # Python dependencies (Markdown placeholder)