import re
from typing import List

def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and normalizing
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove URLs temporarily if needed
    # text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    return text.strip()

def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extract keywords from text (simple implementation)
    """
    # Remove punctuation and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    # Filter by minimum length and remove common stop words
    stop_words = {'и', 'в', 'не', 'на', 'я', 'что', 'он', 'она', 'это', 'как', 'а', 'но', 'они', 'мы', 'вы', 'с', 'у', 'по', 'за', 'до', 'о', 'из', 'от'}
    keywords = [word for word in words if len(word) >= min_length and word not in stop_words]
    return keywords