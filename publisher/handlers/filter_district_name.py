"""Filter district by name handlers."""

import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from publisher.components import districts, presenter, storage, translation

logger = logging.getLogger(__file__)
router = Router()


@router.callback_query(lambda callback: callback.data and callback.data.startswith('filters:district_name:show:'))
async def filter_change_district_name(query: CallbackQuery) -> None:
    """Show change district (by names)."""
    logger.info('filter_change_district_name')
    filters_config = storage.get_user_settings(query.from_user.id)
    page = int(query.data.split(':')[-1])  # type: ignore
    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description.district', filters_config.lang),
        reply_markup=await presenter.get_filters_district_name_menu(query.from_user.id, page),
    )


@router.callback_query(lambda callback: callback.data and callback.data == 'filters:district_name:reset')
@router.callback_query(lambda callback: callback.data and callback.data.startswith('filters:district_name:switch:'))
async def filter_change_district_name_switch(query: CallbackQuery) -> None:  # noqa: WPS213
    """Process change district (by names)."""
    filters_config = storage.get_user_settings(query.from_user.id)
    logger.info(f'filter_change_district_name_switch {query.data=} {filters_config.district_names=}')
    district_for_switch = query.data.split(':')[-1]  # type: ignore

    if district_for_switch == 'reset':
        logger.info('filter_change_district_name_switch: reset')
        if filters_config.district_names is not None:
            storage.update_user_settings(user_id=query.from_user.id, district_names=None)
            await _refresh_page(query)
        return None

    available_names = await districts.get_district_names()
    if district_for_switch not in available_names:
        logger.error('invalid district name value got!')
        return None

    if filters_config.district_names is None:
        logger.info('filter_change_district_name_switch: enable from not set')
        storage.update_user_settings(
            user_id=query.from_user.id,
            district_names={district_for_switch},
            districts=None,
        )
        return await _refresh_page(query)

    if district_for_switch in filters_config.district_names:
        new_value = (filters_config.district_names - {district_for_switch}) or None
        logger.info(f'filter_change_district_name_switch: disable, {new_value=}')
        storage.update_user_settings(
            user_id=query.from_user.id,
            district_names=new_value,
            districts=None,
        )
        return await _refresh_page(query)

    new_value = filters_config.district_names | {district_for_switch}
    logger.info(f'filter_change_district_name_switch: enable, {new_value=}')
    storage.update_user_settings(
        user_id=query.from_user.id,
        district_names=new_value,
        districts=None,
    )
    return await _refresh_page(query)


async def _refresh_page(query: CallbackQuery) -> None:
    try:
        page = int(query.data.split(':')[-2])  # type: ignore
    except ValueError:
        page = 1
    await query.message.edit_reply_markup(  # type: ignore
        reply_markup=await presenter.get_filters_district_name_menu(query.from_user.id, page),
    )
