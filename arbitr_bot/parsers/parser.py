import re
from typing import Dict, List, Optional
from ..categories.categorizer import categorize_text

def parse_announcement(text: str) -> Dict[str, str]:
    """
    Parse announcement text to extract title and content.
    This is a simple implementation - can be enhanced based on specific channel formats.
    """
    # Split text into lines
    lines = text.split('\n')
    
    # Assume first non-empty line is title (or first few words)
    title = ""
    content_lines = []
    
    for line in lines:
        line = line.strip()
        if line and not title:
            # Take first substantial line as title (or first few words)
            title = ' '.join(line.split()[:10])  # First 10 words as title
        elif line:
            content_lines.append(line)
    
    content = '\n'.join(content_lines) if content_lines else text
    
    # Determine category
    category = categorize_text(text)
    
    return {
        "title": title,
        "content": content,
        "category": category
    }

def extract_links(text: str) -> List[str]:
    """
    Extract URLs from text
    """
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_pattern, text)