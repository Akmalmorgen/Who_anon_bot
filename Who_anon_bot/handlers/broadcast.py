from telegram.ext import MessageHandler, filters
from utils.media import broadcast_media
from states.states import get_state, set_state
from config.settings import ADMINS

async def ask_broadcast(update, context):
    uid = update.effective_user.id
    if uid not in ADMINS:
        return

    set_state(uid, "BROADCAST")
    await update.message.reply_text("Отправьте сообщение для рассылки:")

async def do_broadcast(update, context):
    uid = update.effective_user.id
    if get_state(uid) != "BROADCAST":
        return

    await broadcast_media(context, update.message)
    await update.message.reply_text("Готово!")

def register_broadcast_handlers(app):
    app.add_handler(MessageHandler(filters.Regex("📢 Рассылка"), ask_broadcast))
    app.add_handler(MessageHandler(filters.ALL, do_broadcast))
