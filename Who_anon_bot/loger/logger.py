# who_anon_bot/logger/logger.py

import logging

# Создаём логгер
logger = logging.getLogger("WhoAnonBot")
logger.setLevel(logging.INFO)

# Формат логов
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# Потоковый хендлер (вывод в консоль)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Добавляем хендлер к логгеру
logger.addHandler(console_handler)

logger.info("Логгер успешно инициализирован.")
