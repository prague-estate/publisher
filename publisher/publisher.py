"""Get estates and publish them to specified telegram channels."""
import asyncio
import logging
from collections import Counter

from aiogram import Bot, exceptions

from publisher.components import api_client, presenter, storage
from publisher.components.types import Estate, Subscription
from publisher.settings import app_settings

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
    logger.info('got {0} active subs'.format(len(active_subs)))

    for category, dst_channel in dst_channels.items():
        ads_for_publish = await api_client.fetch_estates(category=category, limit=limit)
        logger.info('got {0} {1} ads'.format(len(ads_for_publish), category))
        counters[f'{category} total'] = len(ads_for_publish)

        new_ads = _apply_new_only_filter(ads_for_publish)[::-1]
        logger.info('got {0} new {1} ads'.format(len(new_ads), category))

        storage.mark_as_posted(ads_ids=[ads_for_post.id for ads_for_post in new_ads])

        if new_ads and active_subs:
            counters[f'{category} subs notifications'] += await _post_ads_to_subscriptions(
                ads=new_ads,
                subs=active_subs,
            )

        if new_ads:
            counters[f'{category} channel notifications'] += await _post_ads_to_channel(
                ads=new_ads,
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
            post_settings = presenter.get_estate_post_settings(ads_for_post)
            await bot_instance.send_photo(
                chat_id=destination,
                **post_settings,
            )
            cnt += 1
            await asyncio.sleep(3)
    return cnt


async def _post_ads_to_subscriptions(ads: list[Estate], subs: list[Subscription]) -> int:
    cnt = 0
    async with Bot(app_settings.BOT_TOKEN) as bot_instance:
        for ads_for_post in ads:
            for sub in subs:
                user_filters = storage.get_user_settings(sub.user_id)
                logger.debug(f'send notification check {sub=} {ads_for_post=} {user_filters=}')
                if not user_filters.is_enabled_notifications or not user_filters.is_compatible(ads_for_post):
                    continue

                logger.info(f'send notification by subscription {sub=} {ads_for_post=} {user_filters=}')
                await _send_notify_to_user(
                    bot_instance=bot_instance,
                    user_id=sub.user_id,
                    ads_for_post=ads_for_post,
                )
                cnt += 1
    return cnt


async def _send_notify_to_user(bot_instance: Bot, user_id: int, ads_for_post: Estate) -> None:
    try:
        await bot_instance.send_photo(
            chat_id=user_id,
            **presenter.get_estate_post_settings(ads_for_post),
        )
    except (exceptions.TelegramBadRequest, exceptions.TelegramForbiddenError) as exc:
        if 'chat not found' in exc.message:
            logger.warning('disable user notification - chat not found')
            storage.update_user_settings(user_id, enabled=False)
            return
        if 'bot was blocked by the user' in exc.message:
            logger.warning('disable user notification - bot was blocked')
            storage.update_user_settings(user_id, enabled=False)
            return

        raise exc


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    asyncio.run(publisher(limit=app_settings.PUBLISH_ADS_LIMIT))
