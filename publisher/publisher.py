"""Get estates and publish them to specified telegram channels."""
import asyncio
import logging
from collections import Counter
from typing import Any

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import markdown

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

        new_sale_ads = _apply_new_only_filter(sale_ads)
        logger.info('got {0} new {1} ads'.format(len(new_sale_ads), category))
        counters[f'{category} new'] = len(new_sale_ads)

        if new_sale_ads:
            await _post_ads(
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


async def _post_ads(ads: list[Estate], destination: int) -> int:
    storage.mark_as_posted(ads_ids=[
        ads_for_mark.id
        for ads_for_mark in ads
    ])

    cnt = 0
    async with Bot(app_settings.BOT_TOKEN) as bot:
        for ads_for_post in ads:
            message = _message_presenter(ads_for_post)

            ads_link_btn_txt = InlineKeyboardButton(text='Go to advertisement', url=ads_for_post.page_url)
            ads_link_btn = InlineKeyboardMarkup(
                inline_keyboard=[[ads_link_btn_txt]],
                resize_keyboard=True,
            )

            await bot.send_message(
                chat_id=destination,
                text=message,
                parse_mode='Markdown',
                reply_markup=ads_link_btn,
                disable_web_page_preview=False,
            )
            await asyncio.sleep(3)
            cnt += 1

    return cnt


def _message_presenter(ads: Estate) -> str:
    """Create a post for the bot."""
    messages = [
        f'[{ads.title}]({ads.page_url}), {ads.usable_area} m²',
        f'{ads.price:,} {app_settings.CURRENCY}'.replace(",", " "),
    ]

    return markdown.text(*messages, sep='\n')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    run()
