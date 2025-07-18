"""Bot message presenters."""
import re
from typing import Any, Generator

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import markdown
from aiogram.utils.text_decorations import markdown_decoration

from publisher import storage
from publisher.settings import app_settings, prices_settings
from publisher.translation import get_message
from publisher.types import Estate, UserFilters

MARKDOWN_RISK_CHARS = re.compile(r'[_*\[\]()`>#=|{}!\\]')  # noqa: P103


def get_main_menu(user_id: int) -> ReplyKeyboardMarkup:
    """Return main bot keyboard."""
    sub = storage.get_subscription(user_id)
    is_active = bool(sub and sub.is_active)

    user_filters = storage.get_user_filters(user_id)

    if is_active:
        keyboard = [
            [
                KeyboardButton(text=get_message('menu.filters')),
                KeyboardButton(text=get_message('menu.notify.{0}'.format(
                    'active' if user_filters.is_enabled else 'inactive',
                ))),
            ],
            [
                KeyboardButton(text=get_message('menu.subscription.active')),
                KeyboardButton(text=get_message('menu.about')),
            ],
        ]

    else:
        keyboard = [[
            KeyboardButton(text=get_message('menu.subscription.inactive')),
            KeyboardButton(text=get_message('menu.about')),
        ]]

    if app_settings.is_admin(user_id):
        keyboard.append(
            [KeyboardButton(text=get_message('menu.admin'))],
        )

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
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
            text=get_message('filters.button.category.{0}'.format(
                'enabled' if filters_config.category else 'disabled',
            )),
            callback_data='filters:category:show',
        ),
        InlineKeyboardButton(
            text=get_message('filters.button.min_price.{0}'.format(
                'enabled' if filters_config.min_price else 'disabled',
            )),
            callback_data='filters:min_price:show',
        ),
        InlineKeyboardButton(
            text=get_message('filters.button.max_price.{0}'.format(
                'enabled' if filters_config.max_price else 'disabled',
            )),
            callback_data='filters:max_price:show',
        ),
        InlineKeyboardButton(
            text=get_message('filters.button.layout.{0}'.format(
                'enabled' if filters_config.layouts else 'disabled',
            )),
            callback_data='filters:layout:show',
        ),
        InlineKeyboardButton(
            text=get_message('filters.button.district.{0}'.format(
                'enabled' if filters_config.districts else 'disabled',
            )),
            callback_data='filters:district:show',
        ),
        InlineKeyboardButton(
            # todo handler for this
            text=get_message('filters.button.close'),
            callback_data='filters:close',
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
            text=get_message('filters.button.category.all.{0}'.format(
                'enabled' if filters_config.category is None else 'disabled',
            )),
            callback_data='filters:category:reset',
        ),
        InlineKeyboardButton(
            text=get_message('filters.button.category.lease.{0}'.format(
                'enabled' if filters_config.category == 'lease' else 'disabled',
            )),
            callback_data='filters:category:lease',
        ),
        InlineKeyboardButton(
            text=get_message('filters.button.category.sale.{0}'.format(
                'enabled' if filters_config.category == 'sale' else 'disabled',
            )),
            callback_data='filters:category:sale',
        ),
        InlineKeyboardButton(
            text=get_message('filters.button.back'),
            callback_data='filters:back',
        ),
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [button]
            for button in kb
        ],
        resize_keyboard=True,
    )


def get_filters_layout_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return layouts menu."""
    filters_config = storage.get_user_filters(user_id)
    kb = [
        [InlineKeyboardButton(
            text=get_message('filters.button.layout.all.{0}'.format(
                'enabled' if filters_config.layouts is None else 'disabled',
            )),
            callback_data='filters:layout:reset',
        )],
    ]

    for layout_names in _get_batches(app_settings.ENABLED_LAYOUTS, size=2):
        kb.append([
            InlineKeyboardButton(
                text=get_message('filters.button.layout.{0}.{1}'.format(
                    layout_name,
                    'enabled' if filters_config.layouts and layout_name in filters_config.layouts else 'disabled',
                )),
                callback_data=f'filters:layout:switch:{layout_name}',
            )
            for layout_name in layout_names
        ])

    kb.append(
        [InlineKeyboardButton(
            text=get_message('filters.button.back'),
            callback_data='filters:back',
        )],
    )
    return InlineKeyboardMarkup(
        inline_keyboard=kb,
        resize_keyboard=True,
    )


def get_filters_district_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return districts menu."""
    filters_config = storage.get_user_filters(user_id)
    kb = [
        [InlineKeyboardButton(
            text=get_message('filters.button.district.all.{0}'.format(
                'enabled' if filters_config.districts is None else 'disabled',
            )),
            callback_data='filters:district:reset',
        )],
    ]

    for district_names in _get_batches(app_settings.ENABLED_DISTRICTS, size=2):
        kb.append([
            InlineKeyboardButton(
                text=get_message('filters.button.district.number.{0}'.format(
                    'enabled' if filters_config.districts and district_name in filters_config.districts else 'disabled',
                )).format(district_name),
                callback_data=f'filters:district:switch:{district_name}',
            )
            for district_name in district_names
        ])

    kb.append(
        [InlineKeyboardButton(
            text=get_message('filters.button.back'),
            callback_data='filters:back',
        )],
    )
    return InlineKeyboardMarkup(
        inline_keyboard=kb,
        resize_keyboard=True,
    )


def get_filters_min_price_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return change min price dialog."""
    filters_config = storage.get_user_filters(user_id)

    kb = [
        InlineKeyboardButton(
            text=get_message('filters.button.min_price.all.{0}'.format(
                'enabled' if filters_config.min_price is None else 'disabled',
            )),
            callback_data='filters:min_price:reset',
        ),
        InlineKeyboardButton(
            text=get_message('filters.button.min_price.custom.{0}'.format(
                'enabled' if filters_config.min_price is not None else 'disabled',
            )),
            callback_data='filters:min_price:change',
        ),
        InlineKeyboardButton(
            text=get_message('filters.button.back'),
            callback_data='filters:back',
        ),
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [button]
            for button in kb
        ],
        resize_keyboard=True,
    )


def get_filters_min_price_internal_menu() -> InlineKeyboardMarkup:
    """Return change min price internal menu."""
    kb = [
        InlineKeyboardButton(
            text=get_message('filters.button.back'),
            callback_data='filters:back',
        ),
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [button]
            for button in kb
        ],
        resize_keyboard=True,
    )


def get_filters_max_price_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return change max price dialog."""
    filters_config = storage.get_user_filters(user_id)

    kb = [
        InlineKeyboardButton(
            text=get_message('filters.button.max_price.all.{0}'.format(
                'enabled' if filters_config.max_price is None else 'disabled',
            )),
            callback_data='filters:max_price:reset',
        ),
        InlineKeyboardButton(
            text=get_message('filters.button.max_price.custom.{0}'.format(
                'enabled' if filters_config.max_price is not None else 'disabled',
            )),
            callback_data='filters:max_price:change',
        ),
        InlineKeyboardButton(
            text=get_message('filters.button.back'),
            callback_data='filters:back',
        ),
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [button]
            for button in kb
        ],
        resize_keyboard=True,
    )


def get_filters_max_price_internal_menu() -> InlineKeyboardMarkup:
    """Return change max price internal menu."""
    kb = [
        InlineKeyboardButton(
            text=get_message('filters.button.back'),
            callback_data='filters:back',
        ),
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [button]
            for button in kb
        ],
        resize_keyboard=True,
    )


def get_filters_representation(user_filters: UserFilters) -> str:
    """Return user filters representation."""
    messages = []

    if user_filters.category:
        messages.append(f'Category: `{user_filters.category}`')
    else:
        messages.append('Category: `all`')

    if user_filters.min_price:
        messages.append('Min price: `{0}`'.format(
            get_price_human_value(user_filters.min_price),
        ))
    else:
        messages.append('Min price: `not set`')

    if user_filters.max_price:
        messages.append('Max price: `{0}`'.format(
            get_price_human_value(user_filters.max_price),
        ))
    else:
        messages.append('Max price: `not set`')

    if user_filters.layouts:
        layouts = [
            '`{0}`'.format(
                get_message('filters.button.layout.{0}.disabled'.format(layout_name)),
            )
            for layout_name in user_filters.layouts
            if layout_name in app_settings.ENABLED_LAYOUTS
        ]
        messages.append('Layouts: {0}'.format(', '.join(layouts)))
    else:
        messages.append('Layouts: `all`')

    if user_filters.districts:
        districts = [
            '`{0}`'.format(
                get_message('filters.button.district.number.disabled').format(district_number),
            )
            for district_number in user_filters.districts
            if district_number in app_settings.ENABLED_DISTRICTS
        ]
        messages.append('Districts: {0}'.format(', '.join(districts)))
    else:
        messages.append('Districts: `all`')

    return '\n'.join(messages)


def get_estate_post_settings(ads_for_post: Estate) -> dict[str, Any]:
    """Set up estate message settings."""
    ads_link_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Go to advertisement', url=ads_for_post.page_url)],
        ],
        resize_keyboard=True,
    )
    return {
        'caption': _get_estate_description(ads_for_post),
        'photo': ads_for_post.image_url,
        'parse_mode': 'Markdown',
        'reply_markup': ads_link_btn,
    }


def _get_estate_description(ads: Estate) -> str:
    """Create a post for the bot."""
    energy_rate = ads.energy_rating.upper() if len(ads.energy_rating) == 1 else 'unknown'
    messages = [
        f'New flat for {ads.category}:',
        _get_link_without_quote(ads.address, ads.page_url),
        markdown.bold(get_price_human_value(ads.price)),
        markdown.text(get_price_human_value(
            ads.price // ads.usable_area,
            '{0}/m²'.format(get_message('currency')),
        )),
        markdown.text('{0}  m²\n{1}\nenergy rating: {2}'.format(
            ads.usable_area,
            _get_layout_human_value(ads.layout),
            energy_rate,
        )),
        markdown.text('by {0}'.format(
            _get_link_without_quote(
                _get_source_name_link(ads.source_name),
                ads.page_url,
            ),
        )),
    ]

    return markdown.text(*messages, sep='\n')


def get_price_human_value(price: int | None, currency: str | None = None) -> str:
    """Return human-friendly price string."""
    if not price or price < 0:
        return 'not set'
    if currency is None:
        currency = get_message('currency')

    return '{0:,} {1}'.format(price, currency).replace(',', ' ')  # noqa: C819


def _get_layout_human_value(layout: str) -> str:
    """Return human-friendly layout string."""
    mapa = {
        'one_kk': '1+kk',
        'one_one': '1+1',
        'two_kk': '2+kk',
        'two_one': '2+1',
        'three_kk': '3+kk',
        'three_one': '3+1',
        'four_kk': '4+kk',
        'four_more': '4 & more',
    }
    return mapa.get(layout, 'unique layout')


def _get_source_name_link(source_name: str) -> str:
    """Add to source name domain."""
    mapa = {
        'sreality': 'sreality.cz',
        'bezrealitky': 'bezrealitky.cz',
        'svoboda': 'svoboda-williams.com',
        'expats': 'expats.cz',
        'idnes': 'reality.idnes.cz',
        'engelvoelkers': 'engelvoelkers.com',
        'remax': 'remax-czech.cz',
        'ulovdomov': 'ulovdomov.cz',
        'idealninajemce': 'idealninajemce.cz',
        'ceskereality': 'ceskereality.cz',
    }
    return mapa.get(source_name, 'secret source')


def _get_link_without_quote(title: str, url: str) -> str:
    clear_title = re.sub(
        pattern=MARKDOWN_RISK_CHARS,
        repl='',
        string=title,
    )
    return markdown_decoration.link(value=clear_title, link=url)


def _get_batches(original_items: list[Any], size: int) -> Generator[list[Any], None, None]:
    items_amount = len(original_items)
    yield from (
        original_items[ndx:min(ndx + size, items_amount)]
        for ndx in range(0, items_amount, size)
    )
