from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from config.settings import PROJECT_NAME
from keyboards import main_menu_keyboard
from states import (
    STATE_MAIN_MENU,
    STATE_ANON_CHATTING,
)
from db.users import add_user
from db.links import get_link_owner
from db.anon_chat import create_anon_session


# ======================================
#  🔥 ПРИВЕТСТВИЕ /start
# ======================================

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # Сохраняем пользователя в БД
    add_user(user_id)

    # Проверка: пришёл ли юзер по анонимной ссылке
    args = context.args
    if args and args[0].isdigit():
        return await handle_link_entry(update, context, args[0])

    welcome_text = (
        "╔══════════════════════════╗\n"
        f"║   👻 <b>{PROJECT_NAME}</b>   ║\n"
        "╚══════════════════════════╝\n\n"
        f"Привет, <b>{user.first_name}</b>! 🎭\n\n"
        "Я бот для <u>анонимного общения</u>.\n"
        "Можешь:\n\n"
        "🔗 Создать анонимную ссылку\n"
        "🎲 Общаться в рулетке\n"
        "💬 Быть полностью анонимным\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Выберите действие ниже:"
    )

    context.user_data["state"] = STATE_MAIN_MENU

    await update.message.reply_text(
        welcome_text,
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )


# ======================================
#  🔥 ВХОД ЧЕРЕЗ АНОНИМНУЮ ССЫЛКУ
# ======================================

async def handle_link_entry(update: Update, context: ContextTypes.DEFAULT_TYPE, link_id: str):
    user_id = update.effective_user.id

    owner_id = get_link_owner(link_id)
    if not owner_id:
        return await update.message.reply_text(
            "❌ Эта ссылка недействительна или была изменена.",
            reply_markup=main_menu_keyboard()
        )

    if owner_id == user_id:
        return await update.message.reply_text(
            "❌ Это ваша собственная ссылка!",
            reply_markup=main_menu_keyboard()
        )

    # Создаём анонимную сессию
    create_anon_session(user_id, owner_id)

    # Обновляем state
    context.user_data["state"] = STATE_ANON_CHATTING

    await update.message.reply_text(
        "✅ <b>Вы подключены к анонимному чату!</b>\n\n"
        "Пишите сообщение — владелец ссылки его получит.\n"
        "🔒 Вы остаётесь полностью анонимны.",
        parse_mode="HTML"
    )

    # Уведомляем владельца ссылки
    await context.bot.send_message(
        owner_id,
        "🆕 <b>Новое анонимное подключение!</b>\n"
        "Ожидайте сообщение...",
        parse_mode="HTML"
    )


# ======================================
#  📌 Регистрация handlers
# ======================================

def register_start_handlers(application):
    application.add_handler(CommandHandler("start", cmd_start))
