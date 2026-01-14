"""
Test script to verify the functionality of the arbitr bot without running the Telegram bot
"""
import asyncio
import os
from dotenv import load_dotenv

from arbitr_bot.parsers.collector import AnnouncementCollector
from arbitr_bot.categories.categorizer import categorize_text
from arbitr_bot.parsers.parser import parse_announcement
from arbitr_bot.database.crud import get_announcements_by_category, get_announcements_by_keyword, get_all_categories
from arbitr_bot.database.db import SessionLocal

# Load environment variables
load_dotenv()

def test_functionality():
    print("Testing ArbitrBot functionality...")
    
    # Test categorization
    text1 = "Продаю 2-комнатную квартиру в центре, 60 м2, 3/9 этаж"
    category = categorize_text(text1)
    print(f"Categorization test: '{text1}' -> {category}")
    
    # Test parsing
    parsed = parse_announcement(text1)
    print(f"Parsing test: title='{parsed['title']}', category='{parsed['category']}'")
    
    # Test database operations
    with SessionLocal() as db:
        # Create a test announcement
        from arbitr_bot.database.crud import create_announcement
        announcement = create_announcement(
            db=db,
            title=parsed['title'],
            content=text1,
            category=parsed['category'],
            source_channel="test_channel"
        )
        print(f"Database test: Created announcement with ID {announcement.id}")
        
        # Retrieve by category
        results = get_announcements_by_category(db, "недвижимость")
        print(f"Database test: Found {len(results)} announcements in недвижимость category")
        
        # Get all categories
        categories = get_all_categories(db)
        print(f"Database test: Available categories: {categories}")
    
    print("Functionality tests completed successfully!")

async def test_collector():
    print("\nTesting collector functionality...")
    
    # Get channels to monitor
    channels_env = os.getenv("PARSED_CHANNELS", '["channel1", "channel2"]')
    import json
    channels = json.loads(channels_env)
    
    collector = AnnouncementCollector()
    
    # Test collection from one channel
    saved_count = await collector.collect_from_channel(channels[0] if channels else "test_channel")
    print(f"Collector test: Saved {saved_count} announcements from {channels[0] if channels else 'test_channel'}")
    
    print("Collector tests completed successfully!")

async def main():
    test_functionality()
    await test_collector()

if __name__ == "__main__":
    asyncio.run(main())