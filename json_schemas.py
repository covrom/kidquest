"""
JSON schemas for quest validation
"""

from typing import Dict, Any

# Full quest schema
FULL_QUEST_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "quest": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "startStepId": {"type": "string"},
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "image": {"type": "string"},
                            "text": {"type": "string"},
                            "options": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "text": {"type": "string"},
                                        "nextStepId": {"type": "string"},
                                        "emoji": {"type": "string"}
                                    },
                                    "required": ["text", "nextStepId"]
                                }
                            }
                        },
                        "required": ["id", "image", "text"]
                    }
                }
            },
            "required": ["title", "startStepId", "steps"]
        }
    },
    "required": ["quest"]
}

# New quest step schema
NEW_STEP_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "image": {"type": "string"},
        "text": {"type": "string"},
        "options": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "nextStepId": {"type": "string"},
                    "emoji": {"type": "string"}
                },
                "required": ["text", "nextStepId"]
            }
        }
    },
    "required": ["id", "image", "text", "options"]
}