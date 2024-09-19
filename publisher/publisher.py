"""Get estates and publish them to specified telegram channels."""
import asyncio
import logging
from collections import Counter
from typing import Any

from publisher import api, bot_setup, storage
from publisher.settings import app_settings

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


async def _apply_new_only_filter(ads: list[dict]) -> list[dict]:
    # todo test
    return [
        new_ads
        for new_ads in ads
        if await storage.is_already_posted(_ads_hash(new_ads))
    ]


async def _post_ads(ads: list[dict], destination: int) -> int:
    await storage.mark_as_posted(ads_hashes=[
        _ads_hash(ads_for_mark)
        for ads_for_mark in ads
    ])

    # todo post ads to destination channel
    for ads_for_post in ads:
        await bot_setup.bot.send_message(
            chat_id=destination,
            text=ads_for_post['title'],
        )

    # todo test
    return 0


def _ads_hash(ads: dict) -> str:
    # todo impl
    # todo test
    return 'todo'


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    run()
