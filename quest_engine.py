import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class QuestEngine:
    def __init__(self):
        # For now we'll create a mock implementation that returns sample data
        pass
        
    async def generate_quest(self, requirements: str) -> Optional[Dict[str, Any]]:
        """
        Generate a quest scenario using LLM based on user requirements.
        This is a simplified version for demonstration purposes.
        In production, this would call the OpenRouter API with qwen/qwen3-4b:free model.
        """
        # Mock implementation - in real app this would use OpenRouter
        try:
            # Create a sample quest structure based on requirements
            mock_quest = {
                "quest": {
                    "title": f"Квест о {requirements[:20]}...",
                    "startStepId": "step_1",
                    "steps": [
                        {
                            "id": "step_1",
                            "image": "Маленький дракон летит над лесом",
                            "text": f"Привет! Я маленький дракон по имени Драко. Сегодня мы отправимся в приключение, чтобы узнать больше о {requirements}. Что ты хочешь сделать первым?",
                            "options": [
                                {
                                    "text": "Исследовать лес",
                                    "nextStepId": "step_2a",
                                    "emoji": "🌲"
                                },
                                {
                                    "text": "Посмотреть на животных",
                                    "nextStepId": "step_2b",
                                    "emoji": "🐾"
                                }
                            ]
                        },
                        {
                            "id": "step_2a",
                            "image": "Дракон смотрит вдаль из леса",
                            "text": "Ты исследуешь лес и находишь старое дерево. Оно выглядит очень интересно!",
                            "options": [
                                {
                                    "text": "Подойти ближе",
                                    "nextStepId": "step_3a1",
                                    "emoji": "👉"
                                },
                                {
                                    "text": "Посмотреть на землю вокруг",
                                    "nextStepId": "step_3a2",
                                    "emoji": "🔍"
                                }
                            ]
                        },
                        {
                            "id": "step_2b",
                            "image": "Дракон смотрит на птицу в небе",
                            "text": "Ты видишь красивую птицу, которая летает над тобой!",
                            "options": [
                                {
                                    "text": "Попробовать поймать её",
                                    "nextStepId": "step_3b1",
                                    "emoji": "🕊️"
                                },
                                {
                                    "text": "Подождать и наблюдать",
                                    "nextStepId": "step_3b2",
                                    "emoji": "👀"
                                }
                            ]
                        },
                        # Ending steps
                        {
                            "id": "step_3a1",
                            "image": "Дракон смотрит на старое дерево",
                            "text": "Ты подходишь к дереву и видишь, что оно очень старое. Оно рассказывает тебе историю!",
                            "options": [
                                {
                                    "text": "Слушать историю",
                                    "nextStepId": "ending_1",
                                    "emoji": "👂"
                                },
                                {
                                    "text": "Попробовать сорвать плод",
                                    "nextStepId": "ending_2",
                                    "emoji": "🍎"
                                }
                            ]
                        },
                        {
                            "id": "step_3a2",
                            "image": "Дракон на земле смотрит на насекомых",
                            "text": "Ты находишь интересных насекомых! Они показывают тебе свои особенности.",
                            "options": [
                                {
                                    "text": "Посмотреть поближе",
                                    "nextStepId": "ending_1",
                                    "emoji": "🐛"
                                },
                                {
                                    "text": "Сделать фото",
                                    "nextStepId": "ending_3",
                                    "emoji": "📸"
                                }
                            ]
                        },
                        {
                            "id": "step_3b1",
                            "image": "Дракон с птицей в руках",
                            "text": "Ты пытаешься поймать птицу, но она улетает. Ты понимаешь, что лучше наблюдать за ней!",
                            "options": [
                                {
                                    "text": "Посмотреть на неё издалека",
                                    "nextStepId": "ending_2",
                                    "emoji": "🦅"
                                },
                                {
                                    "text": "Подождать её возвращения",
                                    "nextStepId": "ending_3",
                                    "emoji": "⏳"
                                }
                            ]
                        },
                        {
                            "id": "step_3b2",
                            "image": "Дракон наблюдает за птицей",
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
                        },
                        # Endings
                        {
                            "id": "ending_1",
                            "image": "Дракон с улыбкой в лесу",
                            "text": "Ты узнал много нового и стал лучше понимать мир! Это было замечательное приключение!",
                            "options": []
                        },
                        {
                            "id": "ending_2",
                            "image": "Дракон с плодом в руке",
                            "text": "Ты получил знания о том, как важно уважать природу и не трогать чужое!",
                            "options": []
                        },
                        {
                            "id": "ending_3",
                            "image": "Дракон с рисунком птицы",
                            "text": "Ты сделал отличный рисунок и теперь знаешь, как выглядят эти красивые птицы!",
                            "options": []
                        }
                    ]
                }
            }
            
            return mock_quest
            
        except Exception as e:
            logger.error(f"Error generating quest: {str(e)}")
            return None
    
    async def process_choice(self, current_step: Dict[str, Any], user_choice: str, all_steps: List[Dict]) -> Optional[str]:
        """
        Process user's choice and find the best matching option using LLM.
        This is a simplified version for demonstration purposes.
        In production, this would call the OpenRouter API with qwen/qwen3-4b:free model.
        """
        # Mock implementation - in real app this would use OpenRouter
        try:
            # Simple logic to find matching option (in reality we'd use LLM)
            for option in current_step['options']:
                if user_choice.lower() in option['text'].lower():
                    return option['nextStepId']
            
            # If no match found, return None to trigger new branch creation
            return None
            
        except Exception as e:
            logger.error(f"Error processing choice: {str(e)}")
            return None
    
    async def create_new_branch(self, current_step: Dict[str, Any], user_choice: str, all_steps: List[Dict]) -> Optional[Dict]:
        """
        Create a new branch in the quest when no suitable option is found.
        This is a simplified version for demonstration purposes.
        In production, this would call the OpenRouter API with qwen/qwen3-4b:free model.
        """
        # Mock implementation - in real app this would use OpenRouter
        try:
            # Create a new step based on user's choice (simplified)
            new_step_id = f"step_{len(all_steps) + 1}"
            
            mock_new_step = {
                "id": new_step_id,
                "image": "Новый элемент в приключении",
                "text": f"Ты выбрал: {user_choice}. Это интересное решение! Теперь мы продолжаем наше приключение...",
                "options": [
                    {
                        "text": "Продолжить путь",
                        "nextStepId": new_step_id + "_a",
                        "emoji": "🚶"
                    },
                    {
                        "text": "Посмотреть вокруг",
                        "nextStepId": new_step_id + "_b",
                        "emoji": "👀"
                    }
                ]
            }
            
            return mock_new_step
            
        except Exception as e:
            logger.error(f"Error creating new branch: {str(e)}")
            return None