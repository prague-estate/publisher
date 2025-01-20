"""Bot message presenters."""

import re

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import markdown
from aiogram.utils.text_decorations import markdown_decoration

from publisher import storage
from publisher.settings import prices_settings
from publisher.types import Estate

MARKDOWN_RISK_CHARS = re.compile(r'[_*\[\]()`>#=|{}!\\]')  # noqa: P103

_bot_messages: dict[str, str] = {
    'support': 'For any questions and bugs write direct to @esemiko',
    'support.button': 'About',
    'currency': 'Kč',
    'subscription.button.active': 'Subscription',
    'subscription.button.inactive': '🔴 Subscription',
    'subscription.active': 'Your subscription active through {0}.\nChoose renew option below:',
    'subscription.inactive': 'You have no active subscription yet!\nChoose payment option below:',
    'subscription.expired': 'Your subscription will expire soon!\nShould renew early below:',
    'subscription.downgraded': 'Your subscription was expired!\nChoose payment option below:',
    'invoice.description': 'New estates notifications in your telegram. Fast. Frictionless.',
    'invoice.expired': 'Invoice expired!',
    'invoice.invalid': 'Invoice invalid!',
    'payment.accepted': 'Your subscription has been extended through {0}!',
    'filters.description': 'Set up your estate objects filters for automatic notifications.',
    'filters.button': 'Filters',
    'filters.button.notifications.enabled': 'Notifications: ✅',
    'filters.button.notifications.disabled': 'Notifications: ⏸',
    'filters.button.max_price': 'Max price (Kč)',
}


def get_message(slug: str) -> str:
    """Return message by placeholder."""
    return _bot_messages[slug]


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


def get_prices_menu() -> InlineKeyboardMarkup:
    """Return bot prices inline keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
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
    kb = []
    if filters_config.is_enabled:
        kb.append(
            InlineKeyboardButton(
                text=get_message('filters.button.notifications.enabled'),
                callback_data='filters:enabled',
            ),
        )
    else:
        kb.append(
            InlineKeyboardButton(
                text=get_message('filters.button.notifications.disabled'),
                callback_data='filters:enabled',
            ),
        )

    # todo
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
