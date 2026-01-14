import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from ..database.crud import get_announcements_by_category, get_announcements_by_keyword, get_all_categories
from ..database.db import SessionLocal
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class ArbitrBot:
    def __init__(self, token: str):
        self.token = token
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup command handlers"""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(CommandHandler("categories", self.categories))
        self.application.add_handler(CommandHandler("search", self.search))
        self.application.add_handler(CommandHandler("bycategory", self.by_category))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = (
            "Привет! Я ArbitrBot - бот для поиска объявлений.\n\n"
            "Доступные команды:\n"
            "/categories - Показать все категории\n"
            "/search <ключевое слово> - Поиск по ключевому слову\n"
            "/bycategory <категория> - Показать объявления по категории\n"
            "/help - Помощь"
        )
        await update.message.reply_text(welcome_message)
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = (
            "ArbitrBot - бот для поиска объявлений из различных каналов.\n\n"
            "Команды:\n"
            "/categories - Показать все доступные категории объявлений\n"
            "/search <ключевое слово> - Найти объявления по ключевому слову\n"
            "/bycategory <категория> - Показать объявления в определенной категории\n"
            "/start - Начать работу с ботом"
        )
        await update.message.reply_text(help_message)
    
    async def categories(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show all available categories"""
        with SessionLocal() as db:
            categories = get_all_categories(db)
        
        if categories:
            categories_list = "\n".join([f"- {cat}" for cat in categories])
            await update.message.reply_text(f"Доступные категории:\n{categories_list}")
        else:
            await update.message.reply_text("Пока нет доступных категорий.")
    
    async def search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Search announcements by keyword"""
        if not context.args:
            await update.message.reply_text("Пожалуйста, укажите ключевое слово для поиска. Пример: /search квартира")
            return
        
        keyword = " ".join(context.args)
        
        with SessionLocal() as db:
            announcements = get_announcements_by_keyword(db, keyword)
        
        if announcements:
            response = f"Найдено {len(announcements)} объявлений по запросу '{keyword}':\n\n"
            for ann in announcements[:5]:  # Show first 5 results
                response += f"📁 {ann.title}\n"
                response += f"🏷️ Категория: {ann.category}\n"
                response += f"💬 {ann.content[:100]}...\n\n"
        else:
            response = f"Объявления по запросу '{keyword}' не найдены."
        
        await update.message.reply_text(response)
    
    async def by_category(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show announcements by category"""
        if not context.args:
            await update.message.reply_text("Пожалуйста, укажите категорию. Пример: /bycategory недвижимость")
            return
        
        category = context.args[0].lower()
        
        with SessionLocal() as db:
            announcements = get_announcements_by_category(db, category)
        
        if announcements:
            response = f"Объявления в категории '{category}' ({len(announcements)}):\n\n"
            for ann in announcements[:5]:  # Show first 5 results
                response += f"📁 {ann.title}\n"
                response += f"💬 {ann.content[:100]}...\n\n"
        else:
            response = f"Объявления в категории '{category}' не найдены."
        
        await update.message.reply_text(response)
    
    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Echo any other text message"""
        await update.message.reply_text(
            "Я ArbitrBot. Используйте команды для поиска объявлений:\n"
            "/categories - Показать категории\n"
            "/search <ключевое слово> - Поиск по слову\n"
            "/bycategory <категория> - Объявления по категории"
        )
    
    def run_polling(self):
        """Start the bot in polling mode"""
        logger.info("Starting bot...")
        self.application.run_polling()