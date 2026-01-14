# ArbitrBot - Telegram Advertisement Collector

A Telegram bot that collects advertisements from various channels, categorizes them, stores in a database, and allows users to search and browse them.

## Features

- Collects advertisements from specified Telegram channels
- Automatically categorizes ads based on content
- Stores ads in a SQLite database
- Allows users to search ads by keyword or category
- Provides a simple Telegram bot interface

## Architecture

Simple architecture with the following components:
- `bot/` - Telegram bot implementation
- `database/` - Database models and CRUD operations
- `parsers/` - Ad parsing and collection logic
- `categories/` - Categorization logic
- `utils/` - Utility functions

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your configuration:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
DATABASE_URL=sqlite:///arbitr_bot.db
PARSED_CHANNELS=["channel1", "channel2"]
```

3. Run the bot:
```bash
python -m arbitr_bot.main
```

## Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/categories` - Show all available categories
- `/search <keyword>` - Search ads by keyword
- `/bycategory <category>` - Show ads by category

## Docker Support (Future)

The architecture is designed to be containerizable for deployment on Kubernetes.

## License

MIT