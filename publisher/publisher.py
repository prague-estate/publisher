"""Get estates and publish them to specified telegram channels."""
import asyncio
import logging
from collections import Counter
from typing import Any

from aiogram import Bot, exceptions
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, LinkPreviewOptions

from publisher import api, presenter, storage
from publisher.settings import app_settings
from publisher.types import Estate, Subscription

logger = logging.getLogger(__file__)


async def publisher(limit: int = 1) -> Counter:
    """Fetch ads by API and post them to channels."""
    logger.info('publisher start')
    counters: Counter = Counter()

    dst_channels = {
        'sale': app_settings.PUBLISH_CHANNEL_SALE_ID,
        'lease': app_settings.PUBLISH_CHANNEL_LEASE_ID,
    }
    active_subs = storage.get_active_subscriptions()

    for category, dst_channel in dst_channels.items():
        sale_ads = await api.fetch_estates(category=category, limit=limit)
        logger.info('got {0} {1} ads'.format(len(sale_ads), category))
        counters[f'{category} total'] = len(sale_ads)

        new_sale_ads = _apply_new_only_filter(sale_ads)[::-1]
        logger.info('got {0} new {1} ads'.format(len(new_sale_ads), category))

        storage.mark_as_posted(ads_ids=[ads_for_post.id for ads_for_post in new_sale_ads])

        if new_sale_ads and active_subs:
            counters[f'{category} subs notifications'] += await _post_ads_to_subscriptions(
                ads=new_sale_ads,
                subs=active_subs,
            )

        if new_sale_ads:
            counters[f'{category} channel notifications'] += await _post_ads_to_channel(
                ads=new_sale_ads,
                destination=dst_channel,
            )

    logger.info(f'publisher end {counters=}')

    return counters


def _apply_new_only_filter(ads: list[Estate]) -> list[Estate]:
    return [
        new_ads
        for new_ads in ads
        if storage.is_not_posted_yet(new_ads.id)
    ]


async def _post_ads_to_channel(ads: list[Estate], destination: int) -> int:
    cnt = 0
    async with Bot(app_settings.BOT_TOKEN) as bot_instance:
        for ads_for_post in ads:
            ads_link_btn = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Go to advertisement', url=ads_for_post.page_url)],
                ],
                resize_keyboard=True,
            )

            await bot_instance.send_message(
                chat_id=destination,
                text=presenter.get_estate_description(ads_for_post),
                parse_mode='Markdown',
                reply_markup=ads_link_btn,
                disable_web_page_preview=False,
                link_preview_options=LinkPreviewOptions(
                    prefer_large_media=True,
                ),
            )
            cnt += 1
            await asyncio.sleep(3)
    return cnt


async def _post_ads_to_subscriptions(ads: list[Estate], subs: list[Subscription]) -> int:
    # todo test
    cnt = 0
    async with Bot(app_settings.BOT_TOKEN) as bot_instance:
        for ads_for_post in ads:
            for sub in subs:
                user_filters = storage.get_user_filters(sub.user_id)
                if not user_filters.is_enabled or not user_filters.is_compatible(ads_for_post):
                    continue

                logger.debug(f'send notification by subscription {sub=} {ads_for_post=} {user_filters=}')
                ads_link_btn = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text='Go to advertisement', url=ads_for_post.page_url)],
                    ],
                    resize_keyboard=True,
                )
                await _send_notify_to_user(
                    bot_instance=bot_instance,
                    user_id=sub.user_id,
                    text=presenter.get_estate_description(ads_for_post),
                    parse_mode='Markdown',
                    reply_markup=ads_link_btn,
                    disable_web_page_preview=False,
                    link_preview_options=LinkPreviewOptions(
                        prefer_large_media=True,
                    ),
                )
                cnt += 1
    return cnt


async def _send_notify_to_user(bot_instance: Bot, user_id: int, **kwargs: Any) -> None:
    try:
        await bot_instance.send_message(
            chat_id=user_id,
            **kwargs,
        )
    except exceptions.TelegramBadRequest as exc:
        if 'chat not found' in exc.message:
            storage.update_user_filter(user_id, enabled=False)
            return

        raise exc


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    asyncio.run(publisher(limit=app_settings.PUBLISH_ADS_LIMIT))
