"""Get estates and publish them to specified telegram channels."""
import asyncio
import logging
from itertools import batched

from aiogram import Bot, exceptions
from aiogram.utils import markdown

from publisher.components import api_client, presenter
from publisher.components.types import Estate
from publisher.settings import app_settings

logger = logging.getLogger(__file__)


async def publish() -> None:
    """Fetch ads by API and post them to channels."""
    logger.info('publisher start')
    channels = {
        'sale': app_settings.PUBLISH_CHANNEL_SALE_ID,
        'lease': app_settings.PUBLISH_CHANNEL_LEASE_ID,
    }
    for category, destination in channels.items():
        counters: int = await _publish(category, destination)
        logger.info(f'publisher end {category=} {counters=}')


async def _publish(category: str, destination: int) -> int:
    ads_for_publish = await api_client.fetch_estates(
        limit=app_settings.CHANNEL_ADS_LIMIT,
        category=category,
        without_duplicates=True,
        sliding_window_hours=app_settings.CHANNEL_ADS_SLIDING_WINDOW_HOURS,
    )
    logger.info('got {0} ads'.format(len(ads_for_publish)))
    if not ads_for_publish:
        return 0

    precompiled_ads: list[str] = _prepare_ads_for_post(ads_for_publish)
    await _post_ads_to_channel(
        ads=precompiled_ads,
        destination=destination,
    )
    return len(ads_for_publish)


def _prepare_ads_for_post(ads: list[Estate]) -> list[str]:
    sorted_ads = sorted(ads, key=lambda ads_item: (-ads_item.price, ads_item.is_duplicate))
    return [
        presenter.get_estate_description_short(ads_item, lang='en')
        for ads_item in sorted_ads
    ]


async def _post_ads_to_channel(ads: list[str], destination: int) -> int:
    count = 0
    async with Bot(app_settings.BOT_TOKEN) as bot_instance:
        for batch in batched(ads, n=app_settings.TELEGRAM_MAX_ROWS_PER_MESSAGE):
            try:
                await bot_instance.send_message(
                    chat_id=destination,
                    text=markdown.text(*batch, sep='\n'),
                    parse_mode='Markdown',
                    disable_web_page_preview=True,
                )
                count += 1
            except (exceptions.TelegramBadRequest, exceptions.TelegramForbiddenError) as exc:
                logger.warning('sent to channel error: {0}'.format(exc))
    return count


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    asyncio.run(publish())
