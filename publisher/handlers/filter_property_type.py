"""Filter property type handlers."""

import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from publisher.components import storage, translation, presenter

logger = logging.getLogger(__file__)
router = Router()


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:property_type:show')
async def filter_change_property_type(query: CallbackQuery) -> None:
    """Show change property_type."""
    logger.info('filter_change_property_type')
    settings = storage.get_user_settings(query.from_user.id)

    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description.property_type', settings.lang),
        reply_markup=presenter.get_filters_property_type_menu(query.from_user.id),
    )


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:property_type:flat')
@router.callback_query(lambda callback: callback.data and callback.data == 'filters:property_type:house')
@router.callback_query(lambda callback: callback.data and callback.data == 'filters:property_type:reset')
async def filter_change_property_type_switch(query: CallbackQuery) -> None:
    """Process change property_type."""
    logger.info(f'filter_change_property_type_switch {query.data=}')
    value_for_enable: str = query.data.split(':')[-1]  # type: ignore
    filters_config = storage.get_user_settings(query.from_user.id)

    if value_for_enable == 'reset':
        logger.info('filter_change_property_type_switch: reset')
        if filters_config.property_type is not None:
            storage.update_user_settings(
                user_id=query.from_user.id,
                property_type=None,
                layouts=None,
            )
            return await filter_change_property_type(query)

    elif filters_config.property_type != value_for_enable:
        logger.info(f'filter_change_property_type_switch: enable {value_for_enable}')
        storage.update_user_settings(
            user_id=query.from_user.id,
            property_type=value_for_enable,
            layouts=None,
        )
        return await filter_change_property_type(query)
