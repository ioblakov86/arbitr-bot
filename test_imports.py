"""
Simple test to verify the project structure
"""
def test_imports():
    try:
        from arbitr_bot.database.db import Announcement, engine
        print("✓ Database module imported successfully")
        
        from arbitr_bot.database.crud import create_announcement, get_announcements_by_category
        print("✓ CRUD module imported successfully")
        
        from arbitr_bot.categories.categorizer import categorize_text
        print("✓ Categorizer module imported successfully")
        
        from arbitr_bot.parsers.parser import parse_announcement
        print("✓ Parser module imported successfully")
        
        from arbitr_bot.bot.bot import ArbitrBot
        print("✓ Bot module imported successfully")
        
        from arbitr_bot.parsers.collector import AnnouncementCollector
        print("✓ Collector module imported successfully")
        
        print("\nAll modules imported successfully!")
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        return False

if __name__ == "__main__":
    test_imports()