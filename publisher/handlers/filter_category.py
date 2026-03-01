"""Filter category handlers."""

import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from publisher.components import storage, translation, presenter

logger = logging.getLogger(__file__)
router = Router()


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:category:show')
async def filter_change_category(query: CallbackQuery) -> None:
    """Show change category."""
    logger.info('filter_change_category')
    settings = storage.get_user_settings(query.from_user.id)

    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description.category', settings.lang),
        reply_markup=presenter.get_filters_category_menu(query.from_user.id),
    )


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:category:lease')
@router.callback_query(lambda callback: callback.data and callback.data == 'filters:category:sale')
@router.callback_query(lambda callback: callback.data and callback.data == 'filters:category:reset')
async def filter_change_category_switch(query: CallbackQuery) -> None:
    """Process change category."""
    logger.info(f'filter_change_category_switch {query.data=}')
    category_for_enable: str = query.data.split(':')[-1]  # type: ignore
    filters_config = storage.get_user_settings(query.from_user.id)

    if category_for_enable == 'reset':
        logger.info('filter_change_category_switch: reset')
        if filters_config.category is not None:
            storage.update_user_settings(
                user_id=query.from_user.id,
                category=None,
                min_price=None,
                max_price=None,
            )
            return await filter_change_category(query)

    elif filters_config.category != category_for_enable:
        logger.info(f'filter_change_category_switch: enable {category_for_enable}')
        storage.update_user_settings(
            user_id=query.from_user.id,
            category=category_for_enable,
            min_price=None,
            max_price=None,
        )
        return await filter_change_category(query)
