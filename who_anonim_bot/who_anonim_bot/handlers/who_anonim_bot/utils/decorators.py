from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

from config.settings import ADMINS
from db.users import is_user_banned


# ================================
# 🛡 Декоратор: Только админ
# ================================
def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id

        if user_id not in ADMINS:
            await update.message.reply_text("❌ У вас нет доступа.")
            return

        return await func(update, context, *args, **kwargs)
    return wrapper


# ================================
# ❌ Проверка на бан
# ================================
def require_not_banned(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id

        if is_user_banned(user_id):
            await update.message.reply_text("🚫 Вы заблокированы администраторами.")
            return

        return await func(update, context, *args, **kwargs)
    return wrapper


# ================================
# 📌 Если получили callback — открываем message.chat_id
# ================================
def get_chat_id(update: Update):
    """ Универсальная функция получения chat_id из Update """
    if update.message:
        return update.message.chat_id
    if update.callback_query:
        return update.callback_query.message.chat_id
    return None


# ================================
# 🛡 Декоратор: обработчик только для callback
# ================================
def callback_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not update.callback_query:
            return
        return await func(update, context, *args, **kwargs)
    return wrapper
