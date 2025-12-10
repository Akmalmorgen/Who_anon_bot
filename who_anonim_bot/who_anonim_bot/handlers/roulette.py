from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from states import (
    STATE_ROULETTE_CHOOSE_GENDER,
    STATE_ROULETTE_SEARCH,
    STATE_ROULETTE_CHATTING,
    STATE_MAIN_MENU
)

from keyboards import (
    gender_keyboard,
    roulette_search_keyboard,
    roulette_chat_keyboard,
    main_menu_keyboard
)

from db.roulette import (
    set_user_gender,
    add_to_queue,
    find_match,
    connect_users,
    disconnect_users,
    get_partner,
)

from db.complaints import add_complaint


# ============================================================
# 🔥 НАЧАЛО РУЛЕТКИ
# ============================================================

async def start_roulette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = STATE_ROULETTE_CHOOSE_GENDER

    await update.message.reply_text(
        "🎲 <b>Рулетка</b>\n\nВыберите ваш пол:",
        parse_mode="HTML",
        reply_markup=gender_keyboard()
    )


# ============================================================
# 🔥 ВЫБОР ПОЛА
# ============================================================

async def choose_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "👨 Мужчина":
        gender = "M"
    elif text == "👩 Женщина":
        gender = "F"
    else:
        return

    # сохраняем пол
    set_user_gender(user_id, gender)

    # ищем пару
    partner = find_match(gender)

    if partner:
        # создаём чат
        connect_users(user_id, partner)

        context.user_data["state"] = STATE_ROULETTE_CHATTING
        context.application.user_data.setdefault(partner, {})["state"] = STATE_ROULETTE_CHATTING

        # отправляем обоим
        await update.message.reply_text(
            "✅ <b>Собеседник найден!</b>\nНачинайте общение.",
            parse_mode="HTML",
            reply_markup=roulette_chat_keyboard()
        )

        await context.bot.send_message(
            partner,
            "✅ <b>Собеседник найден!</b>\nНачинайте общение.",
            parse_mode="HTML",
            reply_markup=roulette_chat_keyboard()
        )
        return

    # пары нет → ставим в очередь
    add_to_queue(user_id, gender)
    context.user_data["state"] = STATE_ROULETTE_SEARCH

    await update.message.reply_text(
        "🔍 Ищем собеседника...\nОжидайте.",
        reply_markup=roulette_search_keyboard(),
        parse_mode="HTML"
    )


# ============================================================
# 🔥 СООБЩЕНИЯ В РУЛЕТКЕ
# ============================================================

async def roulette_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    partner = get_partner(user_id)
    if not partner:
        return

    await context.bot.send_message(
        partner,
        f"💬 Собеседник:\n{text}",
        parse_mode="HTML"
    )


# ============================================================
# 🔥 ОТМЕНА ПОИСКА
# ============================================================

async def cancel_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # удаляем из очереди
    disconnect_users(user_id)

    context.user_data["state"] = STATE_MAIN_MENU

    await update.message.reply_text(
        "Поиск отменён.",
        reply_markup=main_menu_keyboard()
    )


# ============================================================
# 🔥 СЛЕДУЮЩИЙ СОБЕСЕДНИК
# ============================================================

async def next_partner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    gender = context.application.user_data[user_id].get("gender", "M")

    # отключаем текущего
    partner = get_partner(user_id)
    if partner:
        disconnect_users(user_id)
        disconnect_users(partner)
        await context.bot.send_message(
            partner,
            "🔄 Собеседник переключился.",
            reply_markup=main_menu_keyboard()
        )

    # и ищем нового
    fake_update = update  # используем структуру set_gender() без изменений
    fake_update.message.text = "👨 Мужчина" if gender == "M" else "👩 Женщина"

    await choose_gender(fake_update, context)


# ============================================================
# 🔥 СТОП — только кнопка СТОП
# ============================================================

async def stop_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    partner = get_partner(user_id)
    if partner:
        disconnect_users(user_id)
        disconnect_users(partner)
        await context.bot.send_message(
            partner,
            "❌ Собеседник завершил чат.",
            reply_markup=main_menu_keyboard()
        )

    context.user_data["state"] = STATE_MAIN_MENU

    await update.message.reply_text(
        "Чат завершён.",
        reply_markup=main_menu_keyboard()
    )


# ============================================================
# 🔥 ЖАЛОБА
# ============================================================

async def roulette_complaint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    partner = get_partner(user_id)
    if not partner:
        return

    # сохраняем жалобу
    add_complaint(f"{user_id}->{partner}", "roulette")

    # сообщаем админам
    for admin in context.bot_data.get("ADMINS", []):
        try:
            await context.bot.send_message(
                admin,
                f"⚠️ <b>Жалоба из рулетки</b>\n"
                f"От <code>{user_id}</code> на <code>{partner}</code>",
                parse_mode="HTML"
            )
        except:
            pass

    await update.message.reply_text("⚠ Жалоба отправлена.")


# ============================================================
# 🔥 ОБРАБОТЧИКИ
# ============================================================

def register_roulette_handlers(application):

    # выбор пола
    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex("^(👨 Мужчина|👩 Женщина)$"),
            choose_gender
        )
    )

    # поиск ― отмена
    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex("^❌ Отменить$"),
            cancel_search
        )
    )

    # чат ― след / стоп / пожаловаться
    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex("^⏭ След. собеседник$"),
            next_partner
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex("^⏹ Стоп$"),
            stop_chat
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex("^⚠️ Пожаловаться$"),
            roulette_complaint
        )
    )

    # обычные сообщения в рулетке
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            roulette_message
        )
  )
