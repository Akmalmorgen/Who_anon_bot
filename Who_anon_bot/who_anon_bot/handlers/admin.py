from telegram.ext import MessageHandler, filters
from keyboards.keyboards import admin_menu
from config.settings import ADMINS
from db.users import list_users, ban, unban
from db.complaints import list_complaints, clear_complaints
from states.states import set_state

async def admin_panel(update, context):
    if update.effective_user.id not in ADMINS:
        return

    set_state(update.effective_user.id, "ADMIN")
    await update.message.reply_text("Админ панель:", reply_markup=admin_menu())

def register_admin_handlers(app):
    app.add_handler(MessageHandler(filters.Regex("📊 Статистика"), admin_panel))
