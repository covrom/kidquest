import json
import logging
import time
from typing import Dict, List, Optional, Any
from openai import OpenAI
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL_NAME

# Import our refactored components - using relative imports from the same directory
from json_schemas import FULL_QUEST_SCHEMA, NEW_STEP_SCHEMA
from prompts import (
    get_quest_generation_prompt,
    get_choice_matching_prompt,
    get_new_branch_prompt
)
from json_utils import extract_json_from_response, extract_choice_result
from quest_validation import is_valid_quest_graph

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
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                # Prepare the prompt for generating quest
                prompt = get_quest_generation_prompt(requirements, user_language)
                
                # Make the API call using OpenAI client
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=8192
                )
                
                
                # Extract the generated quest from the response
                content = response.choices[0].message.content
                result = extract_json_from_response(str(content), FULL_QUEST_SCHEMA)
                
                # Validate that the quest forms a valid acyclic directed graph
                # with one input and multiple outputs
                if result is not None and not is_valid_quest_graph(result):
                    logger.warning("Generated quest failed validation checks")
                    if attempt < max_retries - 1:
                        logger.warning(f"Quest validation failed (attempt {attempt + 1}). Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        logger.error("Failed quest validation after all retries")
                        return None
                
                # If extraction was successful, return the result
                if result is not None:
                    return result
                # If we get here, JSON extraction failed - retry if not last attempt
                if attempt < max_retries - 1:
                    logger.warning(f"JSON extraction failed for quest generation (attempt {attempt + 1}). Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                else:
                    logger.error("Failed to extract valid JSON after all retries")
                    return None

            except Exception as e:
                # If there's an exception during API call or processing, retry if not last attempt
                if attempt < max_retries - 1:
                    logger.warning(f"Error generating quest (attempt {attempt + 1}): {str(e)}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                else:
                    logger.error(f"Error generating quest after all retries: {str(e)}")
                    return None
    
    async def process_choice(self, current_step: Dict[str, Any], user_choice: str, all_steps: List[Dict], user_language: str = 'ru') -> Optional[str]:
        """
        Process user's choice and find the best matching option using LLM.
        Uses OpenRouter API to determine the most appropriate next step.
        """
        try:
            # First check for exact match with options before calling OpenAI
            for option in current_step.get('options', []):
                if user_choice.lower() == option['text'].lower():
                    return option['nextStepId']
            
            # If no exact match, look for matching step ID in options using substring matching
            for option in current_step.get('options', []):
                if user_choice.lower() in option['text'].lower():
                    return option['nextStepId']
                    
            # Prepare prompt for matching user choice with options (only called when no direct match)
            options_text = "\n".join([f"{i+1}. {opt['text']}" for i, opt in enumerate(current_step.get('options', []))])
            
            # Generate the prompt
            prompt = get_choice_matching_prompt(user_choice, options_text, user_language)

            # Make the API call using OpenAI client
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )

            # Extract the result from the response
            content = response.choices[0].message.content
            
            # Get matched option text
            matched_option_text = extract_choice_result(str(content))
            
            if not matched_option_text:
                return None
                
            # Find matching step ID in options
            for option in current_step.get('options', []):
                if matched_option_text == option['text'].lower() or matched_option_text in option['text'].lower():
                    return option['nextStepId']
            
            return None

        except Exception as e:
            logger.error(f"Error processing choice: {str(e)}")
            return None
    
    def is_quest_finished(self, current_step: Dict[str, Any], all_steps: List[Dict]) -> bool:
        """
        Check if the quest has finished (no more options or ending steps).
        A quest is considered finished when there are no more choices to make.
        """
        # If current step has no options, it's likely an ending
        if not current_step.get('options'):
            return True
            
        # Check if all nextStepId values point to ending steps (ending_*)
        for option in current_step.get('options', []):
            next_step_id = option.get('nextStepId')
            if next_step_id and next_step_id.startswith('ending_'):
                return True
                
        return False
    
    async def create_new_branch(self, current_step: Dict[str, Any], user_choice: str, all_steps: List[Dict], user_language: str = 'ru') -> Optional[Dict]:
        """
        Create a new branch in the quest when no suitable option is found.
        Uses OpenRouter API to generate appropriate content for the new step.
        """
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                # Prepare prompt for creating new branch
                prompt = get_new_branch_prompt(user_choice, current_step.get('text', 'No text'), user_language)

                # Make the API call using OpenAI client
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=8192
                )

                # Extract the generated step from the response
                content = response.choices[0].message.content
                result = extract_json_from_response(str(content), NEW_STEP_SCHEMA)
                
                # If extraction was successful, return the result
                if result is not None:
                    return result
                
                # If we get here, JSON extraction failed - retry if not last attempt
                if attempt < max_retries - 1:
                    logger.warning(f"JSON extraction failed for new branch creation (attempt {attempt + 1}). Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                else:
                    logger.error("Failed to extract valid JSON after all retries for new branch creation")
                    return None

            except Exception as e:
                # If there's an exception during API call or processing, retry if not last attempt
                if attempt < max_retries - 1:
                    logger.warning(f"Error creating new branch (attempt {attempt + 1}): {str(e)}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                else:
                    logger.error(f"Error creating new branch after all retries: {str(e)}")
                    return None