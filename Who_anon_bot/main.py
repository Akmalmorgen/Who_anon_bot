# who_anon_bot/main.py
# Главная точка запуска бота Who?Anonim™

from telegram.ext import Application

from config.settings import TOKEN
from logger.logger import setup_logger

# handlers
from handlers.start import register_start_handlers
from handlers.menu import register_menu_handlers
from handlers.anon_link import register_anon_link_handlers
from handlers.anon_chat import register_anon_chat_handlers
from handlers.roulette import register_roulette_handlers
from handlers.admin import register_admin_handlers
from handlers.broadcast import register_broadcast_handlers


def main():
    """Запуск Telegram-бота Who?Anonim™"""

    setup_logger()

    app = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    register_start_handlers(app)
    register_menu_handlers(app)
    register_anon_link_handlers(app)
    register_anon_chat_handlers(app)
    register_roulette_handlers(app)
    register_admin_handlers(app)
    register_broadcast_handlers(app)

    print("🚀 Bot launched: Who?Anonim™")

    app.run_polling()


if __name__ == "__main__":
    main()
