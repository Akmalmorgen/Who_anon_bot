# who_anon_bot/utils/decorators.py

from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

from who_anon_bot.config.settings import ADMINS
from who_anon_bot.db.users import is_banned


def admin_only(func):
    """Ограничение: только для админов."""

    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id

        if user_id not in ADMINS:
            await update.message.reply_text("⛔ У вас нет доступа.")
            return

        return await func(update, context)

    return wrapper


def check_ban(func):
    """Запретить использовать бота заблокированным."""

    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id

        if is_banned(user_id):
            await update.message.reply_text("🚫 Вы заблокированы администрацией.")
            return

        return await func(update, context)

    return wrapper
