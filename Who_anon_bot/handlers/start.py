from telegram.ext import CommandHandler
from keyboards.keyboards import main_menu
from config.settings import ADMINS
from states.states import set_state

async def start(update, context):
    user = update.effective_user
    set_state(user.id, "MAIN_MENU")

    welcome = (
        "👻 <b>Who?Anonim™ Bot</b>\n\n"
        f"Привет, <b>{user.first_name}</b>!\n"
        "Анонимное общение — здесь.\n\n"
        "Выберите действие 👇"
    )

    await update.message.reply_text(
        welcome,
        parse_mode='HTML',
        reply_markup=main_menu()
    )

def register_start_handlers(app):
    app.add_handler(CommandHandler("start", start))
