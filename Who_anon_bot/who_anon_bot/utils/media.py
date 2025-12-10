# who_anon_bot/utils/media.py

from telegram import Message


async def forward_media(bot, from_chat_id: int, message: Message, to_chat_id: int):
    """
    Универсальная пересылка любого медиа через copy_message.
    Поддерживает:
    - текст
    - фото
    - видео
    - голос
    - аудио
    - документы
    """

    try:
        return await bot.copy_message(
            chat_id=to_chat_id,
            from_chat_id=from_chat_id,
            message_id=message.message_id
        )
    except Exception as e:
        print(f"[MEDIA ERROR] {e}")
        return None
