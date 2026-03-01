"""Filter layout handlers."""

import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from publisher.components import storage, translation, presenter
from publisher.settings import app_settings

logger = logging.getLogger(__file__)
router = Router()


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:layout:show')
async def filter_change_layout(query: CallbackQuery) -> None:
    """Show change layout."""
    logger.info('filter_change_layout')
    settings = storage.get_user_settings(query.from_user.id)

    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description.layout', settings.lang),
        reply_markup=presenter.get_filters_layout_menu(query.from_user.id),
    )


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:layout:reset')
@router.callback_query(lambda callback: callback.data and callback.data.startswith('filters:layout:switch:'))
async def filter_change_layout_switch(query: CallbackQuery) -> None:  # noqa: WPS213
    """Process change layout."""
    filters_config = storage.get_user_settings(query.from_user.id)
    logger.info(f'filter_change_layout_switch {query.data=} {filters_config.layouts=}')
    layout_for_switch: str = query.data.split(':')[-1]  # type: ignore

    if layout_for_switch == 'reset':
        logger.info('filter_change_layout_switch: reset')
        if filters_config.layouts is not None:
            storage.update_user_settings(user_id=query.from_user.id, layouts=None)
            await filter_change_layout(query)
        return None

    if layout_for_switch not in app_settings.ENABLED_LAYOUTS:
        logger.error('invalid layout value got!')
        return None

    if filters_config.layouts is None:
        logger.info('filter_change_layout_switch: enable from not set')
        storage.update_user_settings(
            user_id=query.from_user.id,
            layouts={layout_for_switch},
        )
        return await filter_change_layout(query)

    elif layout_for_switch in filters_config.layouts:
        new_value = (filters_config.layouts - {layout_for_switch}) or None
        logger.info(f'filter_change_layout_switch: disable, {new_value=}')
        storage.update_user_settings(
            user_id=query.from_user.id,
            layouts=new_value,
        )
        return await filter_change_layout(query)

    new_value = filters_config.layouts | {layout_for_switch}
    logger.info(f'filter_change_layout_switch: enable, {new_value=}')
    storage.update_user_settings(
        user_id=query.from_user.id,
        layouts=new_value,
    )
    return await filter_change_layout(query)
