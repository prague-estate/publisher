"""User setting handlers."""

import logging
from itertools import cycle

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from publisher.components import storage, presenter, translation
from publisher.settings import app_settings

logger = logging.getLogger(__file__)
router = Router()


@router.callback_query(lambda callback: callback.data and callback.data == 'settings:toggle:enabled')
async def user_settings_toggle_notifications(query: CallbackQuery) -> None:
    """Change notifications status."""
    logger.info('notifications toggle')
    settings = storage.get_user_settings(query.from_user.id)

    if settings.is_enabled_notifications:
        storage.update_user_settings(query.from_user.id, enabled=False)
    else:
        storage.update_user_settings(query.from_user.id, enabled=True)

    await query.message.edit_reply_markup(  # type: ignore
        reply_markup=presenter.get_settings_menu(query.from_user.id),
    )


@router.callback_query(lambda callback: callback.data and callback.data == 'settings:toggle:skip_duplicates')
async def user_settings_toggle_skip_duplicates(query: CallbackQuery) -> None:
    """Change skip duplicates status."""
    logger.info('skip_duplicates toggle')
    settings = storage.get_user_settings(query.from_user.id)

    if settings.skip_duplicates:
        storage.update_user_settings(query.from_user.id, skip_duplicates=False)
    else:
        storage.update_user_settings(query.from_user.id, skip_duplicates=True)

    await query.message.edit_reply_markup(  # type: ignore
        reply_markup=presenter.get_settings_menu(query.from_user.id),
    )


@router.callback_query(lambda callback: callback.data and callback.data == 'settings:toggle:lang')
async def user_settings_toggle_lang(query: CallbackQuery) -> None:
    """Change user language."""
    logger.info('language toggle')
    settings = storage.get_user_settings(query.from_user.id)

    if settings.lang in app_settings.ENABLED_LANGUAGES:
        langs_cycle = cycle(app_settings.ENABLED_LANGUAGES)
        while True:
            lang = next(langs_cycle)
            if lang == settings.lang:
                storage.update_user_settings(query.from_user.id, lang=next(langs_cycle))
                break
    else:
        storage.update_user_settings(query.from_user.id, lang=app_settings.ENABLED_LANGUAGES[0])

    await query.message.edit_reply_markup(  # type: ignore
        reply_markup=presenter.get_settings_menu(query.from_user.id),
    )


@router.callback_query(lambda callback: callback.data and callback.data == 'settings:close')
async def user_settings_close(query: CallbackQuery, state: FSMContext | None = None) -> None:
    """Close settings."""
    logger.info('settings_close')
    settings = storage.get_user_settings(query.from_user.id)

    if state:
        await state.clear()

    await query.message.delete()  # type: ignore
    await query.message.answer(  # type: ignore
        text=translation.get_i8n_text('settings.updated', settings.lang),
        reply_markup=presenter.get_main_menu(query.from_user.id),
        parse_mode='Markdown',
    )
