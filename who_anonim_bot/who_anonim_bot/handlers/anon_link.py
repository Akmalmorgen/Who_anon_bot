from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from states import (
    STATE_MY_LINK,
    STATE_CHANGE_LINK,
    STATE_ANON_CHATTING
)
from keyboards import anon_link_keyboard, main_menu_keyboard
from db.links import (
    get_or_create_link,
    change_user_link,
    count_link_users
)
from db.anon_chat import close_all_sessions_by_owner


# ==========================================
# 🔥 ОТКРЫТЬ МОЮ АНОНИМНУЮ ССЫЛКУ
# ==========================================

async def open_my_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Получаем существующую или создаём новую
    link_id = get_or_create_link(user_id)

    # Считаем количество подключений
    connected = count_link_users(user_id)

    link = f"https://t.me/{context.bot.username}?start={link_id}"

    text = (
        "🔗 <b>Ваша анонимная ссылка</b>\n\n"
        f"<code>{link}</code>\n"
        f"🆔 ID: <code>{link_id}</code>\n\n"
        f"👥 Подключено: <b>{connected}</b>\n\n"
        "Выберите действие:"
    )

    context.user_data["state"] = STATE_MY_LINK

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=anon_link_keyboard()
    )


# ==========================================
# 🔥 СМЕНА ССЫЛКИ (с кнопкой Отмена)
# ==========================================

async def start_change_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = STATE_CHANGE_LINK

    await update.message.reply_text(
        "🔄 <b>Вы уверены, что хотите сменить ссылку?</b>\n\n"
        "Все текущие анонимные чаты будут закрыты.\n\n"
        "Нажмите ещё раз: <b>Сменить ссылку</b>\n"
        "или ⬅️ Назад для отмены.",
        parse_mode="HTML",
        reply_markup=anon_link_keyboard()
    )


async def confirm_change_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Закрываем все активные анонимные чаты у владельца
    close_all_sessions_by_owner(user_id, context.bot)

    # Создаём новую ссылку
    new_link_id = change_user_link(user_id)

    link = f"https://t.me/{context.bot.username}?start={new_link_id}"

    text = (
        "✅ <b>Ссылка успешно обновлена!</b>\n\n"
        f"🔗 Новая ссылка:\n<code>{link}</code>\n"
        f"🆔 ID: <code>{new_link_id}</code>"
    )

    context.user_data["state"] = STATE_MY_LINK

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=anon_link_keyboard()
    )


# ==========================================
# 🔥 ОБРАБОТЧИК СООБЩЕНИЙ ДЛЯ ЭТОГО РАЗДЕЛА
# ==========================================

async def process_anon_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    state = context.user_data.get("state")

    if state == STATE_MY_LINK:
        if text == "🔄 Сменить ссылку":
            return await start_change_link(update, context)
        return  # всё остальное игнорируется

    if state == STATE_CHANGE_LINK:
        if text == "🔄 Сменить ссылку":
            return await confirm_change_link(update, context)
        return  # не трогаем "Назад", он в menu.py


# ==========================================
# 🔥 РЕГИСТРАЦИЯ
# ==========================================

def register_anon_link_handlers(application):
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, process_anon_link)
  )
