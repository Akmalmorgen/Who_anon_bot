from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from states import (
    STATE_MAIN_MENU,
    STATE_MY_LINK,
    STATE_ROULETTE_CHOOSE_GENDER,
)
from keyboards import main_menu_keyboard
from handlers.anon_link import open_my_link
from handlers.roulette import start_roulette
from handlers.start import cmd_start
from config.settings import ADMINS
from handlers.admin import open_admin_panel
from handlers.start import cmd_start


# ================================
# 🔥 ОБРАБОТКА ГЛАВНОГО МЕНЮ
# ================================

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    state = context.user_data.get("state", STATE_MAIN_MENU)

    # Назад → возвращение в главное меню
    if text == "🔙 Назад":
        context.user_data["state"] = STATE_MAIN_MENU
        return await update.message.reply_text(
            "Главное меню:",
            reply_markup=main_menu_keyboard()
        )

    # --- Главное меню ---
    if state == STATE_MAIN_MENU:

        if text == "🔗 Моя анон-ссылка":
            return await open_my_link(update, context)

        if text == "🎲 Рулетка":
            context.user_data["state"] = STATE_ROULETTE_CHOOSE_GENDER
            return await start_roulette(update, context)

        if text == "💬 Помощь":
            return await show_help(update, context)

        # Админ-кнопка (если админ)
        if text == "⚙️ Админ-панель" and user_id in ADMINS:
            return await open_admin_panel(update, context)

    # Если ни один вариант не подошёл:
    return await update.message.reply_text(
        "Выберите действие на клавиатуре:",
        reply_markup=main_menu_keyboard()
    )


# ================================
# 🔥 Помощь
# ================================

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):

    help_text = (
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💡 <b>ПОМОЩЬ</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔗 <u>Анонимная ссылка:</u>\n"
        "• Создайте свою ссылку\n"
        "• Отправьте её кому угодно\n"
        "• Получайте анонимные сообщения\n\n"
        "🎲 <u>Рулетка:</u>\n"
        "• Общение с незнакомцами\n"
        "• Полная анонимность\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "👨‍💻 <i>Партнёрство, доработка, помощь:</i>\n"
        "📱 @who_mercy\n"
        "━━━━━━━━━━━━━━━━━━━━━━━"
    )

    await update.message.reply_text(
        help_text,
        parse_mode="HTML",
        reply_markup=main_menu_keyboard()
    )


# ================================
# 🔥 РЕГИСТРАЦИЯ
# ================================

def register_menu_handlers(application):
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
