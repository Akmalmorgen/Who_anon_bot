# main.py
# Главная точка запуска бота Who?Anonim™

from telegram.ext import Application

# Токен и настройки
from config.settings import TOKEN

# Логер
from logger.logger import setup_logger

# Группы обработчиков
from handlers.start import register_start_handlers
from handlers.menu import register_menu_handlers
from handlers.anon_link import register_anon_link_handlers
from handlers.anon_chat import register_anon_chat_handlers
from handlers.roulette import register_roulette_handlers
from handlers.admin import register_admin_handlers
from handlers.broadcast import register_broadcast_handlers


def main():
    """Запуск Telegram-бота."""

    # Включаем логирование
    setup_logger()

    # Создаём приложение Telegram Bot API
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    register_start_handlers(application)
    register_menu_handlers(application)
    register_anon_link_handlers(application)
    register_anon_chat_handlers(application)
    register_roulette_handlers(application)
    register_admin_handlers(application)
    register_broadcast_handlers(application)

    print("🚀 Who?Anonim™ Bot успешно запущен!")

    # Запускаем polling
    application.run_polling()


if __name__ == "__main__":
    main()
