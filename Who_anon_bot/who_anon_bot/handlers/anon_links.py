import random
from telegram.ext import MessageHandler, filters
from keyboards.keyboards import anon_link_menu
from db.links import get_or_create_link, update_link
from states.states import set_state

async def send_my_link(update, context):
    user_id = update.effective_user.id

    link_id = get_or_create_link(user_id)
    link = f"https://t.me/Who_Anonim_Bot?start={link_id}"

    set_state(user_id, "ANON_LINK_MENU")

    await update.message.reply_text(
        f"🔗 Ваша анонимная ссылка:\n<code>{link}</code>\n\n"
        "🟦 Управление ссылкой:",
        parse_mode='HTML',
        reply_markup=anon_link_menu()
    )

async def change_link(update, context):
    user_id = update.effective_user.id

    new_id = str(random.randint(100000, 999999))
    update_link(user_id, new_id)

    link = f"https://t.me/Who_Anonim_Bot?start={new_id}"

    await update.message.reply_text(
        "🔄 <b>Ссылка обновлена!</b>\n\n"
        f"🔗 Новая: <code>{link}</code>",
        parse_mode='HTML',
        reply_markup=anon_link_menu()
    )

def register_anon_link_handlers(app):
    app.add_handler(MessageHandler(filters.Regex("🔄 Сменить ссылку"), change_link))
