"""Filter prices handlers."""

import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from publisher.components import storage, translation, presenter, forms

logger = logging.getLogger(__file__)
router = Router()


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:min_price:show')
async def filter_change_min_price(query: CallbackQuery) -> None:
    """Show change min price."""
    logger.info('filter_change_min_price')
    settings = storage.get_user_settings(query.from_user.id)

    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description.min_price', settings.lang).format(
            presenter.get_price_human_value(settings.min_price, settings.lang),
        ),
        reply_markup=presenter.get_filters_min_price_menu(query.from_user.id),
    )


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:min_price:reset')
async def filter_change_min_price_reset(query: CallbackQuery) -> None:
    """Reset min price filter to default value."""
    logger.info(f'filter_change_min_price_reset {query.data=}')
    filters_config = storage.get_user_settings(query.from_user.id)
    if filters_config.min_price is not None:
        storage.update_user_settings(user_id=query.from_user.id, min_price=None)
        return await filter_change_min_price(query)


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:min_price:change')
async def filter_change_min_price_change(query: CallbackQuery, state: FSMContext) -> None:
    """Change min price filter value input."""
    logger.info('filter_change_min_price_change')
    await state.set_state(forms.Form.min_price)

    settings = storage.get_user_settings(query.from_user.id)
    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description.min_price.input', settings.lang),
        reply_markup=presenter.get_filters_min_price_internal_menu(query.from_user.id),
    )


@router.message(forms.Form.min_price)
async def filter_change_min_price_change_process(message: Message, state: FSMContext) -> None:
    """Change min price filter value processing."""
    logger.info('filter_change_min_price_change_process')

    try:
        threshold = int(message.text.strip().lower())  # type: ignore

    except (ValueError, AttributeError):
        threshold = 0

    settings = storage.get_user_settings(message.chat.id)

    if threshold <= 0:
        await message.reply(translation.get_i8n_text('filters.description.min_price.invalid', settings.lang))
        return

    storage.update_user_settings(user_id=message.chat.id, min_price=threshold)
    await state.clear()

    await message.answer(  # type: ignore
        text=translation.get_i8n_text('filters.description.min_price', settings.lang).format(
            presenter.get_price_human_value(threshold, settings.lang),
        ),
        reply_markup=presenter.get_filters_min_price_menu(message.chat.id),
    )


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:max_price:show')
async def filter_change_max_price(query: CallbackQuery) -> None:
    """Show change max price."""
    logger.info('filter_change_max_price')
    settings = storage.get_user_settings(query.from_user.id)

    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description.max_price', settings.lang).format(
            presenter.get_price_human_value(settings.max_price, settings.lang),
        ),
        reply_markup=presenter.get_filters_max_price_menu(query.from_user.id),
    )


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:max_price:reset')
async def filter_change_max_price_reset(query: CallbackQuery) -> None:
    """Reset max price filter to default value."""
    logger.info(f'filter_change_max_price_reset {query.data=}')
    filters_config = storage.get_user_settings(query.from_user.id)
    if filters_config.max_price is not None:
        storage.update_user_settings(user_id=query.from_user.id, max_price=None)
        return await filter_change_max_price(query)


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:max_price:change')
async def filter_change_max_price_change(query: CallbackQuery, state: FSMContext) -> None:
    """Change max price filter value input."""
    logger.info('filter_change_max_price_change')
    await state.set_state(forms.Form.max_price)

    filters_config = storage.get_user_settings(query.from_user.id)
    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description.max_price.input', filters_config.lang),
        reply_markup=presenter.get_filters_max_price_internal_menu(query.from_user.id),
    )


@router.message(forms.Form.max_price)
async def filter_change_max_price_change_process(message: Message, state: FSMContext) -> None:
    """Change max price filter value processing."""
    logger.info('filter_change_max_price_change_process')
    settings = storage.get_user_settings(message.chat.id)

    try:
        threshold = int(message.text.strip().lower())  # type: ignore
    except (ValueError, AttributeError):
        threshold = 0

    if threshold <= 0:
        await message.reply(translation.get_i8n_text('filters.description.max_price.invalid', settings.lang))
        return

    storage.update_user_settings(user_id=message.chat.id, max_price=threshold)
    await state.clear()

    await message.answer(  # type: ignore
        text=translation.get_i8n_text('filters.description.max_price', settings.lang).format(
            presenter.get_price_human_value(threshold, settings.lang),
        ),
        reply_markup=presenter.get_filters_max_price_menu(message.chat.id),
    )
