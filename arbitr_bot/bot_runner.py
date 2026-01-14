#!/usr/bin/env python3
"""
ArbitrBot - Telegram Bot for Advertisement Collection and Search

This bot collects advertisements from various Telegram channels,
categorizes them, stores in a database, and allows users to search
and browse them.
"""

import logging
import os
from dotenv import load_dotenv

from arbitr_bot.bot.bot import ArbitrBot

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Main function to start the bot"""
    # Get bot token from environment variable
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
    
    # Initialize bot
    bot = ArbitrBot(bot_token)
    
    # Start bot
    try:
        logger.info("Starting bot...")
        bot.run_polling()
    except KeyboardInterrupt:
        logger.info("Shutting down...")

if __name__ == "__main__":
    main()