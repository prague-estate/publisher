"""Callback queries handlers."""

import logging

from aiogram import Dispatcher, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from publisher.components import forms, presenter, storage, translation

logger = logging.getLogger(__file__)
router = Router()


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:min_usable_area:show')
async def filter_change_min_usable_area(query: CallbackQuery) -> None:
    """Show change min usable area."""
    logger.info('filter_change_min_usable_area')

    filters_config = storage.get_user_settings(query.from_user.id)

    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description.min_usable_area', filters_config.lang).format(
            filters_config.min_usable_area or 0,
        ),
        reply_markup=presenter.get_filters_min_usable_area_menu(query.from_user.id),
    )


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:min_usable_area:reset')
async def filter_change_min_usable_area_reset(query: CallbackQuery) -> None:
    """Reset min usable are filter to default value."""
    logger.info(f'filter_change_min_usable_area_reset {query.data=}')
    filters_config = storage.get_user_settings(query.from_user.id)
    if filters_config.min_usable_area is not None:
        storage.update_user_settings(user_id=query.from_user.id, min_usable_area=None)
        return await filter_change_min_usable_area(query)


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:min_usable_area:change')
async def filter_change_min_usable_area_change(query: CallbackQuery, state: FSMContext) -> None:
    """Change min usable area filter value input."""
    logger.info('filter_change_min_usable_area_change')
    await state.set_state(forms.Form.min_usable_area)

    filters_config = storage.get_user_settings(query.from_user.id)
    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description.min_usable_area.input', filters_config.lang),
        reply_markup=presenter.get_filters_min_usable_area_internal_menu(query.from_user.id),
    )


@router.message(forms.Form.min_usable_area)
async def filter_change_min_usable_area_change_process(message: Message, state: FSMContext) -> None:
    """Change min usable area filter value processing."""
    logger.info('filter_change_min_usable_area_change_process')
    filters_config = storage.get_user_settings(message.chat.id)

    try:
        threshold = int(message.text.strip().lower())  # type: ignore
    except (ValueError, AttributeError):
        threshold = 0

    if threshold <= 0:
        await message.reply(translation.get_i8n_text('filters.description.min_usable_area.invalid', filters_config.lang))
        return

    storage.update_user_settings(user_id=message.chat.id, min_usable_area=threshold)
    await state.clear()

    await message.answer(  # type: ignore
        text=translation.get_i8n_text('filters.description.min_usable_area', filters_config.lang).format(
            threshold or 0,
        ),
        reply_markup=presenter.get_filters_min_usable_area_menu(message.chat.id),
    )


def init(dp: Dispatcher) -> None:
    """Routers setup."""
    dp.include_router(router)
