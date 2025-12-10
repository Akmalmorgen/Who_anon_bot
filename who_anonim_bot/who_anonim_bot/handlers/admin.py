from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from config.settings import ADMINS
from states import (
    STATE_ADMIN_PANEL,
    STATE_ADMIN_BAN,
    STATE_ADMIN_UNBAN,
)
from keyboards import admin_keyboard, main_menu_keyboard

from db.users import get_all_users, ban_user, unban_user, is_banned
from db.links import count_links
from db.anon_chat import count_active_sessions
from db.roulette import count_active_roulette
from db.complaints import get_complaints, clear_complaints


# ============================================================
# 🔥 ОТКРЫТЬ АДМИН-ПАНЕЛЬ
# ============================================================

async def open_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in ADMINS:
        return await update.message.reply_text("❌ У вас нет доступа.")

    context.user_data["state"] = STATE_ADMIN_PANEL

    total_users = len(get_all_users())
    total_links = count_links()
    total_roulette = count_active_roulette()
    total_complaints = len(get_complaints())

    text = (
        "👑 <b>АДМИН-ПАНЕЛЬ</b>\n\n"
        f"👥 Пользователи: <b>{total_users}</b>\n"
        f"🔗 Активных ссылок: <b>{total_links}</b>\n"
        f"🎲 Чатов в рулетке: <b>{total_roulette}</b>\n"
        f"⚠ Жалоб: <b>{total_complaints}</b>\n"
        "━━━━━━━━━━━━━━━\n"
        "Выберите действие:"
    )

    await update.message.reply_text(text, parse_mode="HTML", reply_markup=admin_keyboard())


# ============================================================
# 🔥 ПРОСМОТР ПОЛЬЗОВАТЕЛЕЙ
# ============================================================

async def admin_show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users = get_all_users()
    text = "👥 <b>Пользователи:</b>\n\n"

    for uid in list(users)[:20]:
        status = "🚫" if is_banned(uid) else "✅"
        text += f"{status} <code>{uid}</code>\n"

    if len(users) > 20:
        text += f"\n...ещё {len(users) - 20}"

    await update.message.reply_text(text, parse_mode="HTML", reply_markup=admin_keyboard())


# ============================================================
# 🔥 ПОКАЗАТЬ ЖАЛОБЫ
# ============================================================

async def admin_show_complaints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    complaints = get_complaints()

    if not complaints:
        return await update.message.reply_text("Жалоб нет ✔", reply_markup=admin_keyboard())

    text = "⚠ <b>Жалобы:</b>\n\n"

    for c in complaints[-20:]:
        text += (
            f"От: <code>{c['user_from']}</code>\n"
            f"На: <code>{c['user_to']}</code>\n"
            f"Причина: <b>{c['reason']}</b>\n"
            "────────────\n"
        )

    await update.message.reply_text(text, parse_mode="HTML", reply_markup=admin_keyboard())


# ============================================================
# 🔥 ОЧИСТИТЬ ЖАЛОБЫ
# ============================================================

async def admin_clear_complaints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_complaints()
    await update.message.reply_text("✔ Жалобы очищены!", reply_markup=admin_keyboard())


# ============================================================
# 🔥 БАН
# ============================================================

async def admin_ban_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = STATE_ADMIN_BAN

    await update.message.reply_text(
        "Введите ID пользователя для бана:",
        reply_markup=admin_keyboard()
    )


async def admin_ban_execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        target_id = int(update.message.text)
    except ValueError:
        return await update.message.reply_text("ID должен быть числом!", reply_markup=admin_keyboard())

    ban_user(target_id)

    await update.message.reply_text(
        f"🚫 Пользователь <code>{target_id}</code> забанен.",
        parse_mode="HTML",
        reply_markup=admin_keyboard()
    )


# ============================================================
# 🔥 РАЗБАН
# ============================================================

async def admin_unban_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = STATE_ADMIN_UNBAN

    await update.message.reply_text(
        "Введите ID пользователя для разбанивания:",
        reply_markup=admin_keyboard()
    )


async def admin_unban_execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        target_id = int(update.message.text)
    except ValueError:
        return await update.message.reply_text("ID должен быть числом!", reply_markup=admin_keyboard())

    unban_user(target_id)

    await update.message.reply_text(
        f"✅ Пользователь <code>{target_id}</code> разбанен.",
        parse_mode="HTML",
        reply_markup=admin_keyboard()
    )


# ============================================================
# 🔥 РЕГИСТРАЦИЯ
# ============================================================

def register_admin_handlers(application):

    # Вход в админку
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^⚙️ Админ-панель$"), open_admin_panel)
    )

    # Показ пользователей
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^👥 Пользователи$"), admin_show_users)
    )

    # Жалобы
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^⚠️ Жалобы$"), admin_show_complaints)
    )

    # Очистить жалобы
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^🗑 Очистить жалобы$"), admin_clear_complaints)
    )

    # Бан
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^🚫 Забанить$"), admin_ban_request)
    )

    # Разбан
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^✅ Разбанить$"), admin_unban_request)
    )

    # Ввести ID (бан)
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            admin_ban_execute
        )
    )

    # Ввести ID (разбан)
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            admin_unban_execute
        )
  )
