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

async def main_async():
    """Async main function to start the bot and collector"""
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

    # Create tasks for both bot and collector
    collector_task = asyncio.create_task(run_collector(channels))

    # Run both tasks concurrently
    try:
        # Run the bot polling in the event loop
        await bot.application.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        collector_task.cancel()
        try:
            await collector_task
        except asyncio.CancelledError:
            pass

def main():
    """Main function to start the bot and collector"""
    # Run the async main function
    asyncio.run(main_async())

if __name__ == "__main__":
    main()