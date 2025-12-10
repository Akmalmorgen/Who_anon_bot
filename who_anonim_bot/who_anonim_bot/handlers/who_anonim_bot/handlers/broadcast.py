from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from config.settings import ADMINS
from states import STATE_ADMIN_PANEL, STATE_BROADCAST
from keyboards import admin_keyboard

from utils.media import forward_media_message


# ============================================================
# 🔥 ЗАПУСК РЕЖИМА РАССЫЛКИ
# ============================================================

async def broadcast_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMINS:
        return await update.message.reply_text("❌ У вас нет доступа.")

    context.user_data["state"] = STATE_BROADCAST

    await update.message.reply_text(
        "📢 <b>РАССЫЛКА</b>\n\n"
        "Отправьте текст или любое медиа.\n"
        "Будет отправлено всем пользователям.",
        parse_mode="HTML",
        reply_markup=admin_keyboard()
    )


# ============================================================
# 🔥 ВЫПОЛНЕНИЕ РАССЫЛКИ
# ============================================================

async def broadcast_execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMINS:
        return

    # Проверяем состояние
    if context.user_data.get("state") != STATE_BROADCAST:
        return

    message = update.message

    # Получаем всех пользователей
    from db.users import get_all_users, is_banned
    users = get_all_users()

    sent = 0
    failed = 0

    await update.message.reply_text("📨 Рассылка началась...")

    for uid in users:
        if is_banned(uid):
            continue

        try:
            # Используем универсальный медиаперенос
            await forward_media_message(context.bot, target_id=uid, message=message)
            sent += 1
        except Exception:
            failed += 1

    context.user_data["state"] = STATE_ADMIN_PANEL

    await update.message.reply_text(
        f"📢 <b>Рассылка завершена!</b>\n\n"
        f"✔ Отправлено: <b>{sent}</b>\n"
        f"❌ Ошибок: <b>{failed}</b>",
        parse_mode="HTML",
        reply_markup=admin_keyboard()
    )


# ============================================================
# 🔥 РЕГИСТРАЦИЯ ХЕНДЛЕРОВ
# ============================================================

def register_broadcast_handlers(application):

    # команда "Рассылка"
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^📢 Рассылка$"), broadcast_request)
    )

    # получение медиа/текста
    application.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND,
            broadcast_execute
        )
  )
