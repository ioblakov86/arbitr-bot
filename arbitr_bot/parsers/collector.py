import asyncio
import logging
from typing import Dict, List
from ..database.crud import create_announcement
from ..database.db import SessionLocal
from ..parsers.parser import parse_announcement, extract_links
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnnouncementCollector:
    def __init__(self):
        # In a real implementation, this would connect to Telegram API to read channels
        # For now, we'll simulate with mock data
        pass
    
    async def collect_from_channel(self, channel_name: str):
        """
        Collect announcements from a specific channel.
        This is a simplified version - in reality, you'd connect to Telegram API here.
        """
        logger.info(f"Collecting announcements from {channel_name}")
        
        # Mock data - in real implementation, fetch from actual channels
        mock_announcements = [
            {
                "text": "Продам 2-комнатную квартиру в центре города. 60 м², 3/9 этаж. Цена 8.5 млн руб.",
                "source_url": f"https://t.me/{channel_name}/1"
            },
            {
                "text": "Ищу работу в сфере IT. Опыт 3 года, знание Python, JavaScript",
                "source_url": f"https://t.me/{channel_name}/2"
            },
            {
                "text": "Куплю б/у ноутбук Dell или HP до 30000 рублей. Состояние хорошее.",
                "source_url": f"https://t.me/{channel_name}/3"
            }
        ]
        
        saved_count = 0
        for item in mock_announcements:
            parsed_data = parse_announcement(item["text"])
            
            with SessionLocal() as db:
                try:
                    # Check if announcement already exists (by content hash or similar)
                    # For simplicity, we'll just add all
                    create_announcement(
                        db=db,
                        title=parsed_data["title"],
                        content=item["text"],
                        category=parsed_data["category"],
                        source_channel=channel_name,
                        source_url=item.get("source_url")
                    )
                    saved_count += 1
                except Exception as e:
                    logger.error(f"Error saving announcement: {e}")
        
        logger.info(f"Saved {saved_count} announcements from {channel_name}")
        return saved_count
    
    async def collect_all_channels(self, channels: List[str]):
        """
        Collect announcements from all configured channels
        """
        total_saved = 0
        for channel in channels:
            count = await self.collect_from_channel(channel)
            total_saved += count
            # Small delay between channels to avoid rate limiting
            await asyncio.sleep(1)
        
        logger.info(f"Collection complete. Total saved: {total_saved}")
        return total_saved