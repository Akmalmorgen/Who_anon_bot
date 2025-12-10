from .start import register_start_handlers
from .menu import register_menu_handlers
from .anon_link import register_anon_link_handlers
from .anon_chat import register_anon_chat_handlers
from .roulette import register_roulette_handlers
from .admin import register_admin_handlers
from .broadcast import register_broadcast_handlers

def register_all_handlers(app):
    register_start_handlers(app)
    register_menu_handlers(app)
    register_anon_link_handlers(app)
    register_anon_chat_handlers(app)
    register_roulette_handlers(app)
    register_admin_handlers(app)
    register_broadcast_handlers(app)
