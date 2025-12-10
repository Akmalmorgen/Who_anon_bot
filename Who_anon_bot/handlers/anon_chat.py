from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, MessageHandler, filters

from db.anon_chat import open_session, get_owner_by_session, close_session
from utils.media import forward_message

async def joined_via_link(update, context, link_id):
    user_id = update.effective_user.id
    owner_id = open_session(user_id, link_id)

    # сообщение юзеру
    await update.message.reply_text(
        "Вы подключены к анонимному чату.\nПишите, всё скрыто.",
        reply_markup=None
    )

    # уведомление владельцу
    await context.bot.send_message(
        owner_id,
        "🕶 Новое анонимное сообщение!",
        reply_markup=None
    )

async def send_anon_message(update, context):
    sender = update.effective_user.id
    owner = get_owner_by_session(sender)

    if not owner:
        return

    await forward_message(context, update.message, owner)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💬 Ответить", callback_data=f"reply:{sender}"),
            InlineKeyboardButton("⚠ Пожаловаться", callback_data=f"report:{sender}")
        ]
    ])

    await context.bot.send_message(
        owner,
        f"🕶 Сообщение:",
        reply_markup=keyboard
    )

async def handle_inline_buttons(update, context):
    q = update.callback_query
    data = q.data

    if data.startswith("reply:"):
        target = int(data.split(":")[1])
        context.user_data["reply_to"] = target
        await q.message.reply_text("Напишите ответ:")
        await q.answer()

    elif data.startswith("report:"):
        user = int(data.split(":")[1])
        await q.message.reply_text("Жалоба отправлена админу.")
        await q.answer()

def register_anon_chat_handlers(app):
    app.add_handler(CallbackQueryHandler(handle_inline_buttons))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, send_anon_message))
