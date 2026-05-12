from aiogram import Dispatcher

from publisher.handlers import fallback, filter_category, filter_common, filter_district, filter_district_name, \
    filter_layout, filter_price, filter_property_type, filter_usable_area, payments, user_settings


def init(dp: Dispatcher) -> None:
    """Routers setup."""
    dp.include_router(filter_category.router)
    dp.include_router(filter_common.router)
    dp.include_router(filter_district.router)
    dp.include_router(filter_district_name.router)
    dp.include_router(filter_layout.router)
    dp.include_router(filter_price.router)
    dp.include_router(filter_property_type.router)
    dp.include_router(filter_usable_area.router)
    dp.include_router(payments.router)
    dp.include_router(user_settings.router)
    dp.include_router(fallback.router)  # must be the last one
