"""Get estates and publish them to specified telegram channels."""
import asyncio
import logging
from collections import Counter
from typing import Any

from aiogram import Bot

from publisher import api, storage
from publisher.settings import app_settings
from publisher.types import Estate

logger = logging.getLogger(__file__)


def run(args: Any = None) -> None:
    """Run sreality scrapper."""
    asyncio.run(_publisher())


async def _publisher() -> Counter:
    """Fetch ads by API and post them to channels."""
    logger.info('publisher start')
    counters = Counter(total=0)

    dst_channels = {
        'sale': app_settings.PUBLISH_CHANNEL_SALE_ID,
        'lease': app_settings.PUBLISH_CHANNEL_LEASE_ID,
    }

    for category, dst_channel in dst_channels.items():
        sale_ads = await api.fetch_estates(category=category, limit=100)
        logger.info('got {0} {1} ads'.format(len(sale_ads), category))
        counters[f'{category} total'] = len(sale_ads)

        new_sale_ads = await _apply_new_only_filter(sale_ads)
        logger.info('got {0} new {1} ads'.format(len(new_sale_ads), category))
        counters[f'{category} new'] = len(new_sale_ads)

        if new_sale_ads:
            await _post_ads(
                ads=new_sale_ads,
                destination=dst_channel,
            )

    logger.info(f'publisher end {counters=}')
    return counters


async def _apply_new_only_filter(ads: list[Estate]) -> list[Estate]:
    # todo test
    return [
        new_ads
        for new_ads in ads
        if await storage.is_not_posted_yet(new_ads.id)
    ]


async def _post_ads(ads: list[Estate], destination: int) -> int:
    await storage.mark_as_posted(ads_ids=[
        ads_for_mark.id
        for ads_for_mark in ads
    ])

    # todo post ads to destination channel
    async with Bot(app_settings.BOT_TOKEN) as bot:
        for ads_for_post in ads:
            await bot.send_message(
                chat_id=destination,
                text=ads_for_post.title,
            )

    # todo test
    return 0


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    run()
