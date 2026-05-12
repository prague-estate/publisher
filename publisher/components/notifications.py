"""Logs and notifications."""

from aiogram import Bot

from publisher.settings import app_settings


async def send_logs_notification(message: str) -> None:
    """Send message to the logs channel."""
    if not app_settings.BOT_TOKEN:
        return

    async with Bot(app_settings.BOT_TOKEN) as bot_instance:
        await bot_instance.send_message(
            chat_id=app_settings.LOGS_CHANNEL_ID,
            text=message,
        )
