"""Downgrade subs by expire_at field."""
import asyncio
import logging
from collections import Counter
from typing import Any

from aiogram import Bot, exceptions

from publisher import presenter, storage
from publisher.settings import app_settings

logger = logging.getLogger(__file__)


async def run() -> Counter:
    """Fetch active subscriptions and downgrade if expired."""
    logger.info('downgrade start')
    counters: Counter = Counter()
    subs_for_downgrade = [
        sub
        for sub in storage.get_active_subscriptions()
        if not sub.is_active
    ]
    expired_soon = [
        sub
        for sub in storage.get_active_subscriptions()
        if sub.is_expired_soon
    ]

    async with Bot(app_settings.BOT_TOKEN) as bot_instance:
        for sub_expire_soon in expired_soon:
            counters['expired soon'] += 1
            logger.info(f'expired soon {sub_expire_soon=}')
            await _send_notify(
                bot_instance=bot_instance,
                chat_id=sub_expire_soon.user_id,
                text=presenter.get_message('subscription.expired'),
                reply_markup=presenter.get_prices_menu(),
            )

        for sub_for_stop in subs_for_downgrade:
            storage.stop_subscription(sub_for_stop.user_id)
            counters['downgraded'] += 1
            logger.info(f'downgrade {sub_for_stop=}')
            await _send_notify(
                bot_instance=bot_instance,
                chat_id=sub_for_stop.user_id,
                text=presenter.get_message('subscription.downgraded'),
                reply_markup=presenter.get_main_menu(sub_for_stop.user_id),
            )

    logger.info(f'downgrade end {counters=}')
    return counters


async def _send_notify(bot_instance: Bot, **kwargs: Any) -> None:
    try:
        await bot_instance.send_message(**kwargs)
    except exceptions.TelegramAPIError as exc:
        logger.warning(f'Send notify exception {exc}')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    asyncio.run(run())
