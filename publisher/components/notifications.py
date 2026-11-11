"""Logs and notifications."""
import logging
from collections.abc import Awaitable, Callable
from typing import Any

import aiohttp
from aiogram import Bot, exceptions
from aiogram.types import BufferedInputFile

from publisher.components import presenter
from publisher.components.types import Estate
from publisher.settings import app_settings

logger = logging.getLogger(__file__)

# telegram can't fetch some photos by URL (e.g. `binary/octet-stream` content-type without file extension)
PHOTO_URL_ERRORS = (
    'failed to get HTTP URL content',
    'wrong type of the web page content',
    'wrong file identifier/HTTP URL specified',
)


async def send_logs_notification(message: str) -> None:
    """Send message to the logs channel."""
    if not app_settings.BOT_TOKEN:
        return

    async with Bot(app_settings.BOT_TOKEN) as bot_instance:
        await bot_instance.send_message(
            chat_id=app_settings.LOGS_CHANNEL_ID,
            text=message,
        )


async def send_estate(send_photo: Callable[..., Awaitable[Any]], ads: Estate, lang: str) -> None:
    """Send estate as a photo post, upload the photo by ourselves if telegram can't fetch it by URL."""
    estate_settings = presenter.get_estate_as_post(ads, lang)
    logger.info(f'publish {estate_settings=}')
    try:
        await send_photo(**estate_settings)
    except exceptions.TelegramBadRequest as exc:
        if not any(error in exc.message for error in PHOTO_URL_ERRORS):
            raise

        photo = await _download_photo(ads.image_url)
        if photo is None:
            raise

        logger.info(f'resend estate with uploaded photo {ads.id=}')
        estate_settings['photo'] = photo
        await send_photo(**estate_settings)


async def _download_photo(url: str) -> BufferedInputFile | None:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(app_settings.TIMEOUT)) as session:
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                photo_bytes = await resp.read()
        except Exception as exc:
            logger.warning(f'photo download error {url=} {exc=}')
            return None

    return BufferedInputFile(photo_bytes, filename='photo.jpg')
