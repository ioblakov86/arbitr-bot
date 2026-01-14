import re

# Simple categorization logic
CATEGORIES_KEYWORDS = {
    "недвижимость": ["квартир", "дом", "земел", "аренд", "продаж", "покупк", "недвижим"],
    "транспорт": ["машин", "авто", "мотоцикл", "велосипед", "транспорт", "автомобил"],
    "электроника": ["телефон", "компьют", "планшет", "техник", "электрон", "гаджет"],
    "работа": ["ваканс", "работ", "трудоустройств", "сотрудник", "занятост"],
    "услуги": ["услуг", "ремонт", "строительств", "обслуживан", "помощ"],
    "личные_вещи": ["одежд", "обув", "аксессуар", "личн", "вещ"],
    "животные": ["животн", "собак", "кошк", "питомц"],
    "детские": ["ребен", "детск", "игрушк", "коляск", "школьн"],
    "другое": []
}

def categorize_text(text: str) -> str:
    """
    Categorizes text based on keywords.
    Returns the most likely category for the text.
    Uses word stems to match different word forms.
    """
    text_lower = text.lower()

    # Check each category for keywords
    for category, keywords in CATEGORIES_KEYWORDS.items():
        if category != "другое":
            for keyword in keywords:
                # Use word boundaries to match whole words or stems
                pattern = r'\b' + re.escape(keyword)
                if re.search(pattern, text_lower, re.IGNORECASE):
                    return category

    # If no specific category matched, return 'другое'
    return "другое"