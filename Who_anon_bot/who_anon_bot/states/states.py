# who_anon_bot/states/states.py
# Все состояния пользователей

class States:
    MAIN_MENU = "main_menu"

    # Анонимная ссылка
    MY_LINK = "my_anon_link"
    ANON_CHAT = "anon_chat"   # для гостей, пишущих по ссылке

    # Рулетка
    GENDER_SELECT = "gender_select"
    ROULETTE_SEARCH = "roulette_search"
    ROULETTE_ACTIVE = "roulette_active"

    # Админ-панель
    ADMIN_MENU = "admin_menu"
    ADMIN_BAN = "admin_ban"
    ADMIN_UNBAN = "admin_unban"
    ADMIN_BROADCAST = "admin_broadcast"

    # Технические состояния
    UNKNOWN = "unknown"
