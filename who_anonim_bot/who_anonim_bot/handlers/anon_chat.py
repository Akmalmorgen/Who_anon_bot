from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, MessageHandler, CallbackQueryHandler, filters

from states import (
    STATE_ANON_CHATTING,
    STATE_MAIN_MENU
)

from db.anon_chat import (
    get_partner_of_owner,
    get_owner_of_anon,
    save_owner_reply,
    save_anon_message,
)
from db.complaints import add_complaint
from keyboards import main_menu_keyboard


# ============================================================
# 🔥 СОЗДАНИЕ INLINE КНОПОК
# ============================================================

def inline_reply_keyboard(session_id: str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💬 Ответить", callback_data=f"reply:{session_id}"),
            InlineKeyboardButton("⚠ Пожаловаться", callback_data=f"report:{session_id}")
        ]
    ])


def inline_report_keyboard(session_id: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔘 Мат", callback_data=f"report_reason:{session_id}:mat")],
        [InlineKeyboardButton("🔘 Спам", callback_data=f"report_reason:{session_id}:spam")],
        [InlineKeyboardButton("🔘 18+ контент", callback_data=f"report_reason:{session_id}:18")],
        [InlineKeyboardButton("🔘 Угроза", callback_data=f"report_reason:{session_id}:threat")],
    ])


# ============================================================
# 🔥 АНОНИМ ОТПРАВЛЯЕТ СООБЩЕНИЕ
# ============================================================

async def anon_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id  # аноним
    text = update.message.text

    # Кто владелец ссылки?
    owner_id, session_id = get_owner_of_anon(user_id)

    if not owner_id:
        return await update.message.reply_text(
            "❌ Ошибка сессии. Попробуйте снова.",
            reply_markup=main_menu_keyboard()
        )

    # Сохраняем сообщение в БД
    save_anon_message(session_id, user_id, text)

    # Отправляем владельцу
    await context.bot.send_message(
        owner_id,
        f"🕶 <b>Аноним #{session_id}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"{text}\n"
        "━━━━━━━━━━━━━━━━━━",
        parse_mode="HTML",
        reply_markup=inline_reply_keyboard(session_id)
    )

    await update.message.reply_text("Сообщение отправлено анонимно ✔")


# ============================================================
# 🔥 ВЛАДЕЛЕЦ — ОТВЕТЫ АНОНИМУ
# ============================================================

async def owner_reply_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id  # владелец
    text = update.message.text

    # Найти кому владелец отвечает
    partner_id, session_id = get_partner_of_owner(user_id)

    if not partner_id:
        return await update.message.reply_text(
            "❌ Нет активного анонимного диалога.",
            reply_markup=main_menu_keyboard()
        )

    # Сохраняем в БД
    save_owner_reply(session_id, user_id, text)

    # Отправляем анониму
    await context.bot.send_message(
        partner_id,
        f"💬 <b>Ответ владельца:</b>\n{text}",
        parse_mode="HTML"
    )

    await update.message.reply_text("Ответ отправлен ✔")


# ============================================================
# 🔥 CALLBACK: нажали «Ответить»
# ============================================================

async def callback_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    session_id = query.data.split(":")[1]

    context.user_data["reply_to"] = session_id
    context.user_data["state"] = STATE_ANON_CHATTING

    await query.message.reply_text(
        f"✍ Напишите сообщение вашему анониму #{session_id}"
    )


# ============================================================
# 🔥 CALLBACK: нажали «Пожаловаться»
# ============================================================

async def callback_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    session_id = query.data.split(":")[1]

    await query.message.reply_text(
        "Выберите причину жалобы:",
        reply_markup=inline_report_keyboard(session_id)
    )


# ============================================================
# 🔥 CALLBACK: выбрана причина жалобы
# ============================================================

async def callback_report_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, session_id, reason = query.data.split(":")

    add_complaint(session_id, reason)

    await query.message.reply_text("⚠ Жалоба отправлена админу.")


# ============================================================
# 🔥 РЕГИСТРАЦИЯ
# ============================================================

def register_anon_chat_handlers(application):
    application.add_handler(CallbackQueryHandler(callback_reply, pattern=r"^reply:"))
    application.add_handler(CallbackQueryHandler(callback_report, pattern=r"^report:"))
    application.add_handler(CallbackQueryHandler(callback_report_reason, pattern=r"^report_reason:"))

    # Аноним → пишет владельцу
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            anon_message
        )
    )

    # Владелец → отвечает анониму
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            owner_reply_text
        )
          )
