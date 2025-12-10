"""
Главная точка запуска бота Who?Anonim™
"""

from telegram.ext import Application, MessageHandler, CommandHandler, filters

from config.settings import BOT_TOKEN
from logger import get_logger
from handlers.start.start import start_handler
from handlers.menu.menu import menu_handler
from handlers.anon_link.anon_link import anon_link_handler
from handlers.anon_chat.anon_chat import anon_chat_handler
from handlers.roulette.roulette import roulette_handler
from handlers.admin.admin import admin_handler
from handlers.broadcast.broadcast import broadcast_handler

log = get_logger(__name__)


async def unknown(update, context):
    await update.message.reply_text("❓ Неизвестная команда. Используйте меню.")


def main():
    log.info("🚀 Запуск Who?Anonim™ Bot...")

    application = Application.builder().token(BOT_TOKEN).build()

    # Команды
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("admin", admin_handler))

    # Основные текстовые обработчики
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anon_link_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anon_chat_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, roulette_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_handler))

    # Неизвестные команды
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    application.run_polling()
    log.info("Бот успешно запущен.")


if __name__ == "__main__":
    main()
