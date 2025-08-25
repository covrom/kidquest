"""
Prompt templates for quest engine operations
"""

def get_quest_generation_prompt(requirements: str, language: str = 'ru') -> str:
    """Generate prompt for creating a new quest based on requirements."""
    if language == 'en':
        return f"""
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

Return the response strictly in valid JSON format, without extra text, comments or explanations.
Make sure the JSON conforms to the standard (double quotes, correct structure, commas, etc.).

Important:
- Use only English language
- Make the scenario friendly and motivating for children
- Each step should contain 2-3 choice options
- Endings must be positive and educational
"""
    else:  # Default to Russian
        return f"""
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

Верни ответ строго в виде валидного JSON, без лишнего текста, комментариев или пояснений.
Убедись, что JSON соответствует стандарту (двойные кавычки, правильная структура, запятые и т.д.).

Важно:
- Используй только русский язык
- Сделай сценарий дружелюбным и мотивирующим для детей
- Каждый шаг должен содержать 2-3 варианта выбора
- Концовки должны быть позитивными и образовательными
"""


def get_choice_matching_prompt(user_choice: str, options_text: str, language: str = 'ru') -> str:
    """Generate prompt for matching user choice with available options."""
    if language == 'en':
        return f"""
User selected: "{user_choice}"
                                
Choice options:
{options_text}

Determine which choice option best matches the user's response.
Return only the text of the matching choice option.
If no option fits, return "None".
"""
    else:  # Default to Russian
        return f"""
Пользователь выбрал: "{user_choice}"
                                
Варианты выбора:
{options_text}

Определи, какой вариант выбора наиболее соответствует ответу пользователя.
Верни только текст выбранного варианта.
Если ни один вариант не подходит, верни "None".
"""


def get_new_branch_prompt(user_choice: str, current_step_text: str, language: str = 'ru') -> str:
    """Generate prompt for creating a new quest branch when no suitable option is found."""
    if language == 'en':
        return f"""
User selected: "{user_choice}"

Current step:
{current_step_text}

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

Return the response strictly in valid JSON format, without extra text, comments or explanations.
Make sure the JSON conforms to the standard (double quotes, correct structure, commas, etc.).

Important:
- Use only English language
- Make the scenario friendly and motivating for children
- Each step should contain 2-3 choice options
"""
    else:  # Default to Russian
        return f"""
Пользователь выбрал: "{user_choice}"

Текущий шаг:
{current_step_text}

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

Верни ответ строго в виде валидного JSON, без лишнего текста, комментариев или пояснений.
Убедись, что JSON соответствует стандарту (двойные кавычки, правильная структура, запятые и т.д.).

Важно:
- Используй только русский язык
- Сделай сценарий дружелюбным и мотивирующим для детей
- Каждый шаг должен содержать 2-3 варианта выбора
"""