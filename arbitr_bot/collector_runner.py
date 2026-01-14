#!/usr/bin/env python3
"""
Script to run the announcement collector separately
"""

import asyncio
import logging
import os
from dotenv import load_dotenv

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

async def main():
    """Main function to start the collector"""
    # Get channels to monitor
    channels_env = os.getenv("PARSED_CHANNELS", '["channel1", "channel2"]')
    import json
    channels = json.loads(channels_env)
    
    logger.info(f"Starting collector for channels: {channels}")
    
    # Start collector
    await run_collector(channels)

if __name__ == "__main__":
    asyncio.run(main())