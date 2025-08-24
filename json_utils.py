"""
JSON parsing utilities for quest engine operations
"""

import json
import logging
from typing import Dict, Any, Optional

import jsonschema
from jsonschema import ValidationError

logger = logging.getLogger(__name__)

def extract_json_from_response(content: str, schema: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
    """
    Extract JSON from API response content, handling markdown code blocks.
    
    Args:
        content (str): Raw response content from API
        schema (Optional[Dict]): JSON schema to validate against
        
    Returns:
        Optional[Dict[str, Any]]: Parsed JSON data or None if failed
    """
    if content is None:
        logger.error("API response content is None")
        return None
    
    try:
        # Try direct parsing first
        parsed_json = json.loads(content)
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Failed to parse API response: {str(e)}")
        # Try to extract JSON from markdown if it's wrapped in code blocks
        try:
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = content[start:end]
                parsed_json = json.loads(json_str)
            else:
                return None
        except Exception as parse_error:
            logger.error(f"Failed to extract JSON from response: {str(parse_error)}")
            return None
    
    # Validate against schema if provided
    if schema is not None:
        try:
            jsonschema.validate(parsed_json, schema)
        except ValidationError as e:
            logger.error(f"JSON validation failed: {str(e)}")
            return None
    
    return parsed_json

def extract_choice_result(content: str) -> Optional[str]:
    """
    Extract choice result from process_choice API response.
    
    Args:
        content (str): Raw response content from API
        
    Returns:
        Optional[str]: The matched option text or None
    """
    if content is None:
        logger.error("API response content is None in process_choice")
        return None
    
    try:
        result = content.strip().lower()
        
        # Check for "none" responses
        if "none" in result or "не подходит" in result or "ничего не подходит" in result:
            return None
        
        return result
    except Exception as e:
        logger.error(f"Error parsing process_choice response: {str(e)}")
        return None