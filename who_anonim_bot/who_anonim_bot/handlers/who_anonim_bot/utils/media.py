from telegram import Message, Bot


async def forward_media_message(bot: Bot, target_id: int, message: Message):
    """
    Универсальная функция пересылки любого сообщения.
    Используется для:
    - рассылки
    - общения через анонимную ссылку
    - ответов владельца
    """

    # 📝 Текст
    if message.text:
        return await bot.send_message(
            chat_id=target_id,
            text=message.text,
            parse_mode="HTML"
        )

    # 🖼 Фото
    if message.photo:
        return await bot.send_photo(
            chat_id=target_id,
            photo=message.photo[-1].file_id,
            caption=message.caption or "",
            parse_mode="HTML"
        )

    # 🎥 Видео
    if message.video:
        return await bot.send_video(
            chat_id=target_id,
            video=message.video.file_id,
            caption=message.caption or "",
            parse_mode="HTML"
        )

    # 🎞 Анимация (GIF)
    if message.animation:
        return await bot.send_animation(
            chat_id=target_id,
            animation=message.animation.file_id,
            caption=message.caption or "",
            parse_mode="HTML"
        )

    # 📎 Документ
    if message.document:
        return await bot.send_document(
            chat_id=target_id,
            document=message.document.file_id,
            caption=message.caption or "",
            parse_mode="HTML"
        )

    # 🔊 Голосовое
    if message.voice:
        return await bot.send_voice(
            chat_id=target_id,
            voice=message.voice.file_id,
            caption=message.caption or "",
            parse_mode="HTML"
        )

    # 🎵 Аудио
    if message.audio:
        return await bot.send_audio(
            chat_id=target_id,
            audio=message.audio.file_id,
            caption=message.caption or "",
            parse_mode="HTML"
        )

    # 🤳 Видео-заметка
    if message.video_note:
        return await bot.send_video_note(
            chat_id=target_id,
            video_note=message.video_note.file_id
        )

    # 🗳 Опрос
    if message.poll:
        return await bot.send_poll(
            chat_id=target_id,
            question=message.poll.question,
            options=[o.text for o in message.poll.options]
        )

    # 🫂 Стикеры
    if message.sticker:
        return await bot.send_sticker(
            chat_id=target_id,
            sticker=message.sticker.file_id
        )

    # Если формат неизвестен — пересылаем как есть
    return await bot.copy_message(
        chat_id=target_id,
        from_chat_id=message.chat_id,
        message_id=message.message_id
      )
