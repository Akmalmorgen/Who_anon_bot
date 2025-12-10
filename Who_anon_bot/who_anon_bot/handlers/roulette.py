from telegram.ext import MessageHandler, filters
from keyboards.keyboards import gender_menu, roulette_search_menu, roulette_chat_menu
from db.roulette import add_to_queue, match_user, leave_queue
from states.states import set_state

async def start_gender_choose(update, context):
    set_state(update.effective_user.id, "ROULETTE_GENDER")
    await update.message.reply_text("Выберите ваш пол:", reply_markup=gender_menu())

async def gender_selected(update, context):
    user_id = update.effective_user.id
    sex = "M" if update.message.text.startswith("👨") else "F"

    set_state(user_id, "ROULETTE_SEARCH")
    partner = match_user(user_id, sex)

    if partner:
        await update.message.reply_text("Собеседник найден!", reply_markup=roulette_chat_menu())
        await context.bot.send_message(partner, "Собеседник найден!", reply_markup=roulette_chat_menu())
    else:
        add_to_queue(user_id, sex)
        await update.message.reply_text("Поиск...", reply_markup=roulette_search_menu())

def register_roulette_handlers(app):
    app.add_handler(MessageHandler(filters.Regex("👨 Мужчина|👩 Женщина"), gender_selected))
