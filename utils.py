import re
from typing import Optional

def detect_language(text: str) -> str:
    """
    Detect the language of the given text.
    Returns language code (e.g., 'ru', 'en') or 'unknown' if undetermined.
    """
    if not text:
        return 'unknown'
        
    # Count Cyrillic characters
    cyrillic_chars = len(re.findall(r'[а-яА-ЯёЁ]', text))
    
    # Count Latin characters  
    latin_chars = len(re.findall(r'[a-zA-Z]', text))
    
    # If more than 50% of characters are Cyrillic, it's Russian
    total_chars = len(text)
    if total_chars > 0 and cyrillic_chars / total_chars > 0.5:
        return 'ru'
        
    # If more than 50% of characters are Latin, it's English
    elif total_chars > 0 and latin_chars / total_chars > 0.5:
        return 'en'
        
    # Default to Russian for this application context
    return 'ru'
