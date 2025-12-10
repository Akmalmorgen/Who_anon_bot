# who_anon_bot/keyboards/keyboards.py

from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# ------------------------------
# Главное меню
# ------------------------------
def main_menu_kb():
    keyboard = [
        [KeyboardButton("🔗 Моя анон-ссылка")],
        [KeyboardButton("🎲 Рулетка")],
        [KeyboardButton("💬 Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ------------------------------
# Моя ссылка (управление)
# ------------------------------
def my_link_kb():
    keyboard = [
        [KeyboardButton("🔄 Сменить ссылку")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ------------------------------
# Inline кнопки — анонимный чат
# ------------------------------

def anon_message_buttons(session_id: str):
    """Показываются под анонимным сообщением: Ответить / Пожаловаться"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💬 Ответить", callback_data=f"reply:{session_id}"),
            InlineKeyboardButton("⚠ Пожаловаться", callback_data=f"report:{session_id}")
        ]
    ])


def report_reasons_kb(session_id: str):
    """Причины жалобы"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🗯 Мат", callback_data=f"reason:mat:{session_id}")],
        [InlineKeyboardButton("📨 Спам", callback_data=f"reason:spam:{session_id}")],
        [InlineKeyboardButton("🔞 18+ контент", callback_data=f"reason:18:{session_id}")],
        [InlineKeyboardButton("⚠ Угроза", callback_data=f"reason:threat:{session_id}")],
    ])


# ------------------------------
# Рулетка — выбор пола
# ------------------------------
def gender_select_kb():
    keyboard = [
        [KeyboardButton("👨 Мужчина"), KeyboardButton("👩 Женщина")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ------------------------------
# Рулетка — поиск
# ------------------------------
def roulette_search_kb():
    keyboard = [
        [KeyboardButton("❌ Отмена")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ------------------------------
# Рулетка — активный чат
# ------------------------------
def roulette_chat_kb():
    keyboard = [
        [KeyboardButton("⏭ След. собеседник")],
        [KeyboardButton("⛔ Стоп"), KeyboardButton("⬅️ Назад")],
        [KeyboardButton("⚠ Пожаловаться")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ------------------------------
# Админ-панель
# ------------------------------
def admin_menu_kb():
    keyboard = [
        [KeyboardButton("📊 Статистика"), KeyboardButton("👥 Пользователи")],
        [KeyboardButton("⚠ Жалобы"), KeyboardButton("🗑 Очистить жалобы")],
        [KeyboardButton("📢 Рассылка"), KeyboardButton("🔗 Все ссылки")],
        [KeyboardButton("🚫 Забанить"), KeyboardButton("✅ Разбанить")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ------------------------------
# Рассылка — отмена
# ------------------------------
def broadcast_cancel_kb():
    keyboard = [[KeyboardButton("❌ Отмена")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
