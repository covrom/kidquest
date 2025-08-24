import json
import logging
from typing import Dict, List, Optional, Any
from openai import OpenAI
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL_NAME

logger = logging.getLogger(__name__)

class QuestEngine:
    def __init__(self):
        # Initialize with real API configuration using OpenAI client
        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL
        )
        self.model_name = MODEL_NAME
        
    async def generate_quest(self, requirements: str, user_language: str = 'ru') -> Optional[Dict[str, Any]]:
        """
        Generate a quest scenario using LLM based on user requirements.
        This uses the OpenRouter API with qwen/qwen3-4b:free model.
        """
        try:
            # Use language from user state instead of detecting it
            detected_language = user_language
            
            # Prepare the prompt for generating quest
            if detected_language == 'en':
                prompt = f"""
                Create a text-based quest for children (ages 5-7) based on the following requirements:

                {requirements}

                The quest should be:
                - Simple and understandable for young children
                - Educational but fun
                - Contain 3-5 main steps with choice options
                - Include interesting characters (animals, magic, nature)
                - Have multiple endings

                Response must be in JSON format with the following structure:
                {{
                    "quest": {{
                        "title": "Quest title",
                        "startStepId": "step_1",
                        "steps": [
                            {{
                                "id": "step_1",
                                "image": "Image description for step",
                                "text": "Scenario text for step",
                                "options": [
                                    {{
                                        "text": "Choice option 1",
                                        "nextStepId": "step_2a",
                                        "emoji": "😀"
                                    }}
                                ]
                            }}
                        ]
                    }}
                }}

                Important:
                - Use only English language
                - Make the scenario friendly and motivating for children
                - Each step should contain 2-3 choice options
                - Endings must be positive and educational
                """
            else:  # Default to Russian
                prompt = f"""
                Создай текстовый квест для детей (возраст 5-7 лет) на основе следующих требований:

                {requirements}

                Квест должен быть:
                - Простым и понятным для маленьких детей
                - Образовательным, но веселым
                - Содержать 3-5 основных шагов с вариантами выбора
                - Иметь интересные образы (животные, магия, природа)
                - Включать несколько концовок

                Ответ должен быть в формате JSON со следующей структурой:
                {{
                    "quest": {{
                        "title": "Название квеста",
                        "startStepId": "step_1",
                        "steps": [
                            {{
                                "id": "step_1",
                                "image": "Описание изображения для шага",
                                "text": "Текст сценария шага",
                                "options": [
                                    {{
                                        "text": "Вариант выбора 1",
                                        "nextStepId": "step_2a",
                                        "emoji": "😀"
                                    }}
                                ]
                            }}
                        ]
                    }}
                }}

                Важно:
                - Используй только русский язык
                - Сделай сценарий дружелюбным и мотивирующим для детей
                - Каждый шаг должен содержать 2-3 варианта выбора
                - Концовки должны быть позитивными и образовательными
                """

            # Make the API call using OpenAI client
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=8192
            )
            
            # Extract the generated quest from the response
            try:
                content = response.choices[0].message.content
                if content is None:
                    logger.error("API response content is None")
                    return None
                quest_data = json.loads(content)
                return quest_data
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Failed to parse API response: {str(e)}")
                # Try to extract JSON from markdown if it's wrapped in code blocks
                content = response.choices[0].message.content
                if content is None:
                    return None
                try:
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start != -1 and end != -1:
                        json_str = content[start:end]
                        quest_data = json.loads(json_str)
                        return quest_data
                except Exception as parse_error:
                    logger.error(f"Failed to extract JSON from response: {str(parse_error)}")
                    return None

        except Exception as e:
            logger.error(f"Error generating quest: {str(e)}")
            return None
    
    async def process_choice(self, current_step: Dict[str, Any], user_choice: str, all_steps: List[Dict], user_language: str = 'ru') -> Optional[str]:
        """
        Process user's choice and find the best matching option using LLM.
        Uses OpenRouter API to determine the most appropriate next step.
        """
        try:
            # Prepare prompt for matching user choice with options
            options_text = "\n".join([f"{i+1}. {opt['text']}" for i, opt in enumerate(current_step.get('options', []))])
            
            # Use language from user state instead of detecting it
            detected_language = user_language
            
            if detected_language == 'en':
                prompt = f"""
                User selected: "{user_choice}"
                
                Current step:
                {current_step.get('text', 'No text')}
                
                Choice options:
                {options_text}
                
                Determine which choice option best matches the user's response.
                Return only the ID of the next step (e.g., "step_2a" or "ending_1").
                If no option fits, return "None".
                """
            else:  # Default to Russian
                prompt = f"""
                Пользователь выбрал: "{user_choice}"
                
                Текущий шаг:
                {current_step.get('text', 'Нет текста')}
                
                Варианты выбора:
                {options_text}
                
                Определи, какой вариант выбора наиболее соответствует ответу пользователя.
                Верни только ID следующего шага (например: "step_2a" или "ending_1").
                Если ни один вариант не подходит, верни "None".
                """

            # Make the API call using OpenAI client
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )

            # Extract the result from the response
            try:
                content = response.choices[0].message.content
                if content is None:
                    logger.error("API response content is None in process_choice")
                    return None
                    
                result = content.strip().lower()
                
                if "none" in result or "не подходит" in result or "ничего не подходит" in result:
                    return None
                    
                # Look for matching step ID in options
                for option in current_step.get('options', []):
                    if user_choice.lower() in option['text'].lower():
                        return option['nextStepId']
                        
                # If no direct match, try to find the best match based on content
                for option in current_step.get('options', []):
                    if any(word in user_choice.lower() for word in option['text'].lower().split()):
                        return option['nextStepId']
                
                return None
                
            except Exception as e:
                logger.error(f"Error parsing process_choice response: {str(e)}")
                return None

        except Exception as e:
            logger.error(f"Error processing choice: {str(e)}")
            return None
    
    async def create_new_branch(self, current_step: Dict[str, Any], user_choice: str, all_steps: List[Dict], user_language: str = 'ru') -> Optional[Dict]:
        """
        Create a new branch in the quest when no suitable option is found.
        Uses OpenRouter API to generate appropriate content for the new step.
        """
        try:
            # Use language from user state instead of detecting it
            detected_language = user_language
            
            # Prepare prompt for creating new branch
            if detected_language == 'en':
                prompt = f"""
                User selected: "{user_choice}"
                
                Current step:
                {current_step.get('text', 'No text')}
                
                Create a new quest step that corresponds to the user's choice.
                The step should be a logical continuation of the story and contain 2-3 choice options.
                
                Response must be in JSON format with the following structure:
                {{
                    "id": "step_new_1",
                    "image": "Image description for new step",
                    "text": "New step scenario text",
                    "options": [
                        {{
                            "text": "Choice option 1",
                            "nextStepId": "step_new_2a",
                            "emoji": "😀"
                        }}
                    ]
                }}

                Important:
                - Use only English language
                - Make the scenario friendly and motivating for children
                - Each step should contain 2-3 choice options
                """
            else:  # Default to Russian
                prompt = f"""
                Пользователь выбрал: "{user_choice}"
                
                Текущий шаг:
                {current_step.get('text', 'Нет текста')}
                
                Создай новый шаг квеста, который соответствует выбору пользователя.
                Шаг должен быть логичным продолжением истории и содержать 2-3 варианта выбора.
                
                Ответ должен быть в формате JSON со следующей структурой:
                {{
                    "id": "step_new_1",
                    "image": "Описание изображения для нового шага",
                    "text": "Текст сценария нового шага",
                    "options": [
                        {{
                            "text": "Вариант выбора 1",
                            "nextStepId": "step_new_2a",
                            "emoji": "😀"
                        }}
                    ]
                }}

                Важно:
                - Используй только русский язык
                - Сделай сценарий дружелюбным и мотивирующим для детей
                - Каждый шаг должен содержать 2-3 варианта выбора
                """

            # Make the API call using OpenAI client
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=8192
            )

            # Extract the generated step from the response
            try:
                content = response.choices[0].message.content
                if content is None:
                    logger.error("API response content is None in create_new_branch")
                    return None
                new_step_data = json.loads(content)
                return new_step_data
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Failed to parse create_new_branch API response: {str(e)}")
                # Try to extract JSON from markdown if it's wrapped in code blocks
                content = response.choices[0].message.content
                if content is None:
                    return None
                try:
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start != -1 and end != -1:
                        json_str = content[start:end]
                        new_step_data = json.loads(json_str)
                        return new_step_data
                except Exception as parse_error:
                    logger.error(f"Failed to extract JSON from create_new_branch response: {str(parse_error)}")
                    return None

        except Exception as e:
            logger.error(f"Error creating new branch: {str(e)}")
            return None