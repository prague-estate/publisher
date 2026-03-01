"""Common filters buttons."""

import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from publisher.components import presenter, storage, translation, types, api_client
from publisher.settings import app_settings

logger = logging.getLogger(__file__)
router = Router()


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:back')
async def filter_go_back(query: CallbackQuery, state: FSMContext | None = None) -> None:
    """Go back to filters."""
    logger.info('filter_go_back')
    settings = storage.get_user_settings(query.from_user.id)

    if state:
        await state.clear()

    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description', settings.lang),
        reply_markup=presenter.get_filters_menu(query.from_user.id),
    )


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:close')
async def filter_close(query: CallbackQuery, state: FSMContext | None = None) -> None:
    """Close filters."""
    logger.info('filter_close')
    settings = storage.get_user_settings(query.from_user.id)

    if state:
        await state.clear()

    await query.message.delete()  # type: ignore

    logger.info(f'filter_close {settings=}')
    if not settings.is_enabled_notifications:
        await query.message.answer(  # type: ignore
            text=translation.get_i8n_text('filters.set.enable_notifications', settings.lang),
            reply_markup=presenter.get_main_menu(query.from_user.id),
        )
        return

    sub = storage.get_subscription(query.from_user.id)
    logger.info(f'filter_close {sub=}')
    if sub and sub.is_active:
        await _show_last_estate(settings, query.message)  # type: ignore

    await query.message.answer(  # type: ignore
        text=translation.get_i8n_text('notify.enabled', settings.lang).format(
            presenter.get_filters_representation(settings),
        ),
        reply_markup=presenter.get_main_menu(query.from_user.id),
        parse_mode='Markdown',
    )


async def _show_last_estate(filters: types.UserFilters, message: Message) -> None:
    last_ads = await api_client.fetch_estates_all(limit=app_settings.FETCH_ADS_LIMIT)
    logger.info('_show_last_estate: got {0}'.format(len(last_ads)))

    counter = 0
    for ads in last_ads:
        if filters.is_compatible(ads):
            estate_settings = presenter.get_estate_post_settings(ads, filters.lang)
            logger.info(f'publish {estate_settings=}')
            try:
                await message.answer_photo(**estate_settings)
            except Exception as exc:
                logger.error(f'Exception {exc=}')
            counter += 1

        if counter >= app_settings.SHOW_ADS_LIMIT:
            return

    if counter > 0:
        await message.answer(
            text=translation.get_i8n_text('estates.example', filters.lang),
        )
