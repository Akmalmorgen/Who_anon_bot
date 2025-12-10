import logging
import sys


def setup_logger():
    """Создаёт единый логгер для всего бота"""

    logger = logging.getLogger("WhoAnonimBot")
    logger.setLevel(logging.INFO)

    # Формат логов
    formatter = logging.Formatter(
        "%(asctime)s — %(levelname)s — %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Вывод в консоль
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger


# глобальный логгер, который можно импортировать
logger = setup_logger()
