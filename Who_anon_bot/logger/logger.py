# who_anon_bot/logger/logger.py

import logging


def setup_logger():
    """Глобальное логирование для всего бота."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s → %(message)s"
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.info("Логирование успешно инициализировано.")
