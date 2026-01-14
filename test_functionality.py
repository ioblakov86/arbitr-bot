"""
End-to-end functionality test
"""
from arbitr_bot.categories.categorizer import categorize_text
from arbitr_bot.parsers.parser import parse_announcement
from arbitr_bot.database.db import Announcement, SessionLocal
from arbitr_bot.database.crud import create_announcement, get_announcements_by_category

def test_functionality():
    # Test categorization
    text1 = "Продаю 2-комнатную квартиру в центре, 60 м2, 3/9 этаж"
    category = categorize_text(text1)
    print(f"Text: {text1}")
    print(f"Category: {category}")
    assert category == "недвижимость", f"Expected недвижимость, got {category}"
    print("✓ Categorization works correctly")
    
    # Test parsing
    parsed = parse_announcement(text1)
    print(f"Parsed title: {parsed['title']}")
    print(f"Parsed category: {parsed['category']}")
    assert "квартиру" in parsed['title'].lower()
    assert parsed['category'] == "недвижимость"
    print("✓ Parsing works correctly")
    
    # Test database operations
    with SessionLocal() as db:
        # Create a test announcement
        announcement = create_announcement(
            db=db,
            title=parsed['title'],
            content=text1,
            category=parsed['category'],
            source_channel="test_channel"
        )
        print(f"Created announcement with ID: {announcement.id}")
        
        # Retrieve by category
        results = get_announcements_by_category(db, "недвижимость")
        print(f"Found {len(results)} announcements in недвижимость category")
        assert len(results) >= 1
        print("✓ Database operations work correctly")
    
    print("\nAll functionality tests passed!")

if __name__ == "__main__":
    test_functionality()