#!/usr/bin/env python3
"""
ArbitrBot - Telegram Bot for Advertisement Collection and Search

This bot collects advertisements from various Telegram channels,
categorizes them, stores in a database, and allows users to search
and browse them.
"""

import asyncio
import logging
import os
from dotenv import load_dotenv

from arbitr_bot.bot.bot import ArbitrBot
from arbitr_bot.parsers.collector import AnnouncementCollector

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def run_collector(channels):
    """Run the announcement collector periodically"""
    collector = AnnouncementCollector()
    while True:
        try:
            await collector.collect_all_channels(channels)
            # Wait for 1 hour before next collection
            await asyncio.sleep(3600)
        except Exception as e:
            logger.error(f"Error in collector: {e}")
            # Wait for 5 minutes before retrying
            await asyncio.sleep(300)

def main():
    """Main function to start the bot and collector"""
    # Get bot token from environment variable
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

    # Get channels to monitor
    channels_env = os.getenv("PARSED_CHANNELS", '["channel1", "channel2"]')
    import json
    channels = json.loads(channels_env)

    # Initialize bot
    bot = ArbitrBot(bot_token)

    # Start collector in background
    collector_task = asyncio.create_task(run_collector(channels))

    # Start bot
    try:
        bot.run_polling()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        collector_task.cancel()

if __name__ == "__main__":
    main()