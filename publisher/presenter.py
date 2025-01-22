"""Bot message presenters."""

import re

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import markdown
from aiogram.utils.text_decorations import markdown_decoration

from publisher import storage
from publisher.settings import prices_settings
from publisher.translation import get_message
from publisher.types import Estate

MARKDOWN_RISK_CHARS = re.compile(r'[_*\[\]()`>#=|{}!\\]')  # noqa: P103


def get_main_menu(user_id: int) -> ReplyKeyboardMarkup:
    """Return main bot keyboard."""
    sub = storage.get_subscription(user_id)
    is_active = bool(sub and sub.is_active)

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_message('subscription.button.active' if is_active else 'subscription.button.inactive')),
                KeyboardButton(text=get_message('filters.button')),
            ],
            [KeyboardButton(text=get_message('support.button'))],
        ],
        is_persistent=True,
        resize_keyboard=True,
    )


def get_prices_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return bot prices inline keyboard."""
    kb = []
    if not storage.has_used_trial(user_id, 'trial'):
        kb.append([
            InlineKeyboardButton(
                text=get_message('trial'),
                callback_data='trial:activate',
            ),
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=kb + [
            [InlineKeyboardButton(
                text=price.title,
                callback_data=f'buy:{price.cost}',
            )]
            for price in prices_settings.values()
        ],
        resize_keyboard=True,
    )


def get_filters_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return user filters inline keyboard."""
    filters_config = storage.get_user_filters(user_id)
    kb = [
        InlineKeyboardButton(
            text=get_message('filters.button.category'),
            callback_data='filters:category:edit',
        ),
        InlineKeyboardButton(
            text=get_message('filters.button.notifications.{0}'.format(
                'enabled' if filters_config.is_enabled else 'disabled',
            )),
            callback_data='filters:enabled',
        ),
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [button]
            for button in kb
        ],
        resize_keyboard=True,
    )


def get_filters_category_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return change category dialog."""
    filters_config = storage.get_user_filters(user_id)

    kb = [
        InlineKeyboardButton(
            text=get_message(_get_category_slug('rent', filters_config.category)),
            callback_data='filters:category:enable:rent',
        ),
        InlineKeyboardButton(
            text=get_message(_get_category_slug('sale', filters_config.category)),
            callback_data='filters:category:enable:sale',
        ),
    ]

    if filters_config.category is not None:
        kb.append(
            InlineKeyboardButton(
                text=get_message('filters.button.reset'),
                callback_data='filters:category:reset',
            ),
        )

    kb.append(
        InlineKeyboardButton(
            text=get_message('filters.button.back'),
            callback_data='filters:back',
        ),
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [button]
            for button in kb
        ],
        resize_keyboard=True,
    )


def get_estate_description(ads: Estate) -> str:
    """Create a post for the bot."""
    messages = [
        '{0}\n{1} {2}'.format(
            _get_link_without_quote(ads.title, ads.page_url),
            f'{ads.price:,}'.replace(',', ' '),  # noqa: C819
            get_message('currency'),
        ),
    ]
    return markdown.text(*messages, sep='\n')


def _get_link_without_quote(title: str, url: str) -> str:
    clear_title = re.sub(
        pattern=MARKDOWN_RISK_CHARS,
        repl='',
        string=title,
    )
    return markdown_decoration.link(value=clear_title, link=url)


def _get_category_slug(category: str, current_state: str | None) -> str:
    if current_state is None:
        return 'filters.button.category.{0}.enabled'.format(category)

    return 'filters.button.category.{0}.{1}'.format(
        category,
        'enabled' if category == current_state else 'disabled',
    )
