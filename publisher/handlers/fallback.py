"""Fallback handler for unknown messages."""
import logging

from aiogram import Router
from aiogram.types import Message

from publisher.components import presenter, storage, translation

logger = logging.getLogger(__file__)

router = Router()


@router.message()
async def error_handler(message: Message) -> None:
    """Handle stale  and unknown buttons."""
    logger.info('Error handler')
    settings = storage.get_user_settings(message.chat.id)

    await message.answer(
        text=translation.get_i8n_text('error.unknown_button', settings.lang),
        reply_markup=presenter.get_main_menu(message.chat.id),
    )
