"""Filter district handlers."""

import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from publisher.components import storage, translation, presenter
from publisher.settings import app_settings

logger = logging.getLogger(__file__)
router = Router()


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:district:show')
async def filter_change_district(query: CallbackQuery) -> None:
    """Show change district."""
    logger.info('filter_change_district')
    settings = storage.get_user_settings(query.from_user.id)

    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description.district', settings.lang),
        reply_markup=presenter.get_filters_district_menu(query.from_user.id),
    )


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:district:reset')
@router.callback_query(lambda callback: callback.data and callback.data.startswith('filters:district:switch:'))
async def filter_change_district_switch(query: CallbackQuery) -> None:  # noqa: WPS213
    """Process change district."""
    filters_config = storage.get_user_settings(query.from_user.id)
    logger.info(f'filter_change_district_switch {query.data=} {filters_config.districts=}')
    district_for_switch = query.data.split(':')[-1]  # type: ignore

    if district_for_switch == 'reset':
        logger.info('filter_change_district_switch: reset')
        if filters_config.districts is not None:
            storage.update_user_settings(user_id=query.from_user.id, districts=None)
            await filter_change_district(query)
        return None

    if not district_for_switch.isdigit() or int(district_for_switch) not in app_settings.ENABLED_DISTRICTS:
        logger.error('invalid district value got!')
        return None

    district_for_switch = int(district_for_switch)
    if filters_config.districts is None:
        logger.info('filter_change_district_switch: enable from not set')
        storage.update_user_settings(
            user_id=query.from_user.id,
            districts={district_for_switch},
        )
        return await filter_change_district(query)

    elif district_for_switch in filters_config.districts:
        new_value = (filters_config.districts - {district_for_switch}) or None
        logger.info(f'filter_change_district_switch: disable, {new_value=}')
        storage.update_user_settings(
            user_id=query.from_user.id,
            districts=new_value,
        )
        return await filter_change_district(query)

    new_value = filters_config.districts | {district_for_switch}
    logger.info(f'filter_change_district_switch: enable, {new_value=}')
    storage.update_user_settings(
        user_id=query.from_user.id,
        districts=new_value,
    )
    return await filter_change_district(query)
