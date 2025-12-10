from telegram.ext import MessageHandler, filters
from keyboards.keyboards import main_menu
from states.states import get_state, set_state
from handlers.anon_link import send_my_link
from handlers.roulette import start_gender_choose
from handlers.start import start

async def menu_router(update, context):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "🔗 Моя анон-ссылка":
        return await send_my_link(update, context)

    if text == "🎲 Рулетка":
        return await start_gender_choose(update, context)

    if text == "💬 Помощь":
        return await update.message.reply_text(
            "📞 Помощь: @who_mercy",
            reply_markup=main_menu()
        )

def register_menu_handlers(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_router))
