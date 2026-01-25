from aiogram import Dispatcher

from publisher.handlers import filter_usable_area, payments


def init(dp: Dispatcher) -> None:
    """Routers setup."""
    dp.include_router(filter_usable_area.router)
    dp.include_router(payments.router)
