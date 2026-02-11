"""Bot message presenters."""
import re
from typing import Any, Generator

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import markdown
from aiogram.utils.text_decorations import markdown_decoration

from publisher.components import storage
from publisher.components.translation import get_i8n_text
from publisher.components.types import Estate, UserFilters
from publisher.settings import app_settings, prices_settings

MARKDOWN_RISK_CHARS = re.compile(r'[_*\[\]()`>#=|{}!\\]')  # noqa: P103


def get_main_menu(user_id: int) -> ReplyKeyboardMarkup:
    """Return main bot keyboard."""
    sub = storage.get_subscription(user_id)
    settings = storage.get_user_settings(user_id)
    is_active = bool(sub and sub.is_active)

    keyboard = [
        [
            KeyboardButton(text=get_i8n_text('menu.filters', settings.lang)),
            KeyboardButton(text=get_i8n_text('menu.settings', settings.lang)),
        ],
        [
            KeyboardButton(text=get_i8n_text(
                'menu.subscription.{0}'.format('active' if is_active else 'inactive'),
                settings.lang,
            )),
            KeyboardButton(text=get_i8n_text('menu.about', settings.lang)),
        ],
    ]

    if app_settings.is_admin(user_id):
        keyboard.append(
            [KeyboardButton(text=get_i8n_text('menu.admin', settings.lang))],
        )

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        is_persistent=False,
        resize_keyboard=True,
    )


def get_prices_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return bot prices inline keyboard."""
    settings = storage.get_user_settings(user_id)
    kb = []
    if not storage.has_used_trial(user_id, 'trial'):
        kb.append([
            InlineKeyboardButton(
                text=get_i8n_text('trial', settings.lang),
                callback_data='trial:activate',
            ),
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=kb + [
            [InlineKeyboardButton(
                text=get_i8n_text(price.slug, settings.lang),
                callback_data=f'buy:{price.slug}',
            )]
            for price in prices_settings.values()
        ],
        resize_keyboard=True,
    )


def get_settings_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return user settings inline keyboard."""
    user_settings = storage.get_user_settings(user_id)

    notify_button = get_i8n_text(
        'menu.notify.{0}'.format('active' if user_settings.is_enabled_notifications else 'inactive'),
        user_settings.lang,
    )
    lang_button = get_i8n_text('menu.lang.{0}'.format(user_settings.lang), user_settings.lang)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=notify_button, callback_data='settings:toggle:enabled')],
            [InlineKeyboardButton(text=lang_button, callback_data='settings:toggle:lang')],
            [InlineKeyboardButton(
                text=get_i8n_text('filters.button.close', user_settings.lang),
                callback_data='settings:close',
            )],
        ],
        resize_keyboard=True,
    )


def get_filters_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return user filters inline keyboard."""
    filters_config = storage.get_user_settings(user_id)

    kb = [
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.category.{0}'.format('enabled' if filters_config.category else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:category:show',
        ),
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.property_type.{0}'.format('enabled' if filters_config.property_type else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:property_type:show',
        ),
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.min_price.{0}'.format('enabled' if filters_config.min_price else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:min_price:show',
        ),
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.max_price.{0}'.format('enabled' if filters_config.max_price else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:max_price:show',
        ),
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.min_usable_area.{0}'.format(
                    'enabled' if filters_config.min_usable_area else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:min_usable_area:show',
        ),
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.layout.{0}'.format('enabled' if filters_config.layouts else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:layout:show',
        ),
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.district.{0}'.format('enabled' if filters_config.districts else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:district:show',
        ),
        InlineKeyboardButton(
            text=get_i8n_text('filters.button.close', filters_config.lang),
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
    filters_config = storage.get_user_settings(user_id)

    kb = [
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.category.all.{0}'.format('enabled' if filters_config.category is None else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:category:reset',
        ),
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.category.lease.{0}'.format('enabled' if filters_config.category == 'lease' else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:category:lease',
        ),
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.category.sale.{0}'.format('enabled' if filters_config.category == 'sale' else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:category:sale',
        ),
        InlineKeyboardButton(
            text=get_i8n_text('filters.button.back', filters_config.lang),
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


def get_filters_property_type_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return change property_type dialog."""
    filters_config = storage.get_user_settings(user_id)

    kb = [
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.property_type.all.{0}'.format('enabled' if filters_config.property_type is None else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:property_type:reset',
        ),
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.property_type.flat.{0}'.format('enabled' if filters_config.property_type == 'flat' else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:property_type:flat',
        ),
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.property_type.house.{0}'.format('enabled' if filters_config.property_type == 'house' else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:property_type:house',
        ),
        InlineKeyboardButton(
            text=get_i8n_text('filters.button.back', filters_config.lang),
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
    filters_config = storage.get_user_settings(user_id)
    kb = [
        [InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.layout.all.{0}'.format('enabled' if filters_config.layouts is None else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:layout:reset',
        )],
    ]

    for layout_names in _get_batches(app_settings.ENABLED_LAYOUTS, size=2):
        kb.append([
            InlineKeyboardButton(
                text=get_i8n_text(
                    'filters.button.layout.{0}.{1}'.format(
                        layout_name,
                        'enabled' if filters_config.layouts and layout_name in filters_config.layouts else 'disabled',
                    ),
                    filters_config.lang,
                ),
                callback_data=f'filters:layout:switch:{layout_name}',
            )
            for layout_name in layout_names
        ])

    kb.append(
        [InlineKeyboardButton(
            text=get_i8n_text('filters.button.back', filters_config.lang),
            callback_data='filters:back',
        )],
    )
    return InlineKeyboardMarkup(
        inline_keyboard=kb,
        resize_keyboard=True,
    )


def get_filters_district_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return districts menu."""
    filters_config = storage.get_user_settings(user_id)
    kb = [
        [InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.district.all.{0}'.format('enabled' if filters_config.districts is None else 'disabled'),
                filters_config.lang,
            ),
            callback_data='filters:district:reset',
        )],
    ]

    for district_names in _get_batches(app_settings.ENABLED_DISTRICTS, size=2):
        kb.append([
            InlineKeyboardButton(
                text=get_i8n_text(
                    'filters.button.district.number.{0}'.format(
                        'enabled' if filters_config.districts and district_name in filters_config.districts else 'disabled',
                    ),
                    filters_config.lang,
                ).format(district_name),
                callback_data=f'filters:district:switch:{district_name}',
            )
            for district_name in district_names
        ])

    kb.append(
        [InlineKeyboardButton(
            text=get_i8n_text('filters.button.back', filters_config.lang),
            callback_data='filters:back',
        )],
    )
    return InlineKeyboardMarkup(
        inline_keyboard=kb,
        resize_keyboard=True,
    )


def get_filters_min_usable_area_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return change min usable area dialog."""
    filters_config = storage.get_user_settings(user_id)

    kb = [
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.min_usable_area.all.{0}'.format(
                    'enabled' if filters_config.min_usable_area is None else 'disabled',
                ),
                filters_config.lang,
            ),
            callback_data='filters:min_usable_area:reset',
        ),
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.min_usable_area.custom.{0}'.format(
                    'disabled' if filters_config.min_usable_area is None else 'enabled',
                ),
                filters_config.lang,
            ),
            callback_data='filters:min_usable_area:change',
        ),
        InlineKeyboardButton(
            text=get_i8n_text('filters.button.back', filters_config.lang),
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


def get_filters_min_usable_area_internal_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return change min usable area internal menu."""
    filters_config = storage.get_user_settings(user_id)
    kb = [
        InlineKeyboardButton(
            text=get_i8n_text('filters.button.back', filters_config.lang),
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


def get_filters_min_price_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return change min price dialog."""
    filters_config = storage.get_user_settings(user_id)

    kb = [
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.min_price.all.{0}'.format(
                    'enabled' if filters_config.min_price is None else 'disabled',
                ),
                filters_config.lang,
            ),
            callback_data='filters:min_price:reset',
        ),
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.min_price.custom.{0}'.format(
                    'disabled' if filters_config.min_price is None else 'enabled',
                ),
                filters_config.lang,
            ),
            callback_data='filters:min_price:change',
        ),
        InlineKeyboardButton(
            text=get_i8n_text('filters.button.back', filters_config.lang),
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


def get_filters_min_price_internal_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return change min price internal menu."""
    filters_config = storage.get_user_settings(user_id)
    kb = [
        InlineKeyboardButton(
            text=get_i8n_text('filters.button.back', filters_config.lang),
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
    filters_config = storage.get_user_settings(user_id)

    kb = [
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.max_price.all.{0}'.format(
                    'enabled' if filters_config.max_price is None else 'disabled',
                ),
                filters_config.lang,
            ),
            callback_data='filters:max_price:reset',
        ),
        InlineKeyboardButton(
            text=get_i8n_text(
                'filters.button.max_price.custom.{0}'.format(
                    'disabled' if filters_config.max_price is None else 'enabled',
                ),
                filters_config.lang,
            ),
            callback_data='filters:max_price:change',
        ),
        InlineKeyboardButton(
            text=get_i8n_text('filters.button.back', filters_config.lang),
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


def get_filters_max_price_internal_menu(user_id: int) -> InlineKeyboardMarkup:
    """Return change max price internal menu."""
    filters_config = storage.get_user_settings(user_id)
    kb = [
        InlineKeyboardButton(
            text=get_i8n_text('filters.button.back', filters_config.lang),
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

    messages.append('{0}: `{1}`'.format(
        get_i8n_text('filters.name.category', user_filters.lang),
        get_i8n_text('filters.button.category.{0}.disabled'.format(user_filters.category or 'all'), user_filters.lang),
    ))

    messages.append('{0}: `{1}`'.format(
        get_i8n_text('filters.name.property_type', user_filters.lang),
        get_i8n_text('filters.button.property_type.{0}.disabled'.format(user_filters.property_type or 'all'), user_filters.lang),
    ))

    if user_filters.min_price:
        messages.append('{0}: `{1} {2}`'.format(
            get_i8n_text('filters.name.min_price', user_filters.lang),
            get_price_human_value(user_filters.min_price, user_filters.lang),
            get_i8n_text('currency', user_filters.lang),
        ))

    if user_filters.max_price:
        messages.append('{0}: `{1} {2}`'.format(
            get_i8n_text('filters.name.max_price', user_filters.lang),
            get_price_human_value(user_filters.max_price, user_filters.lang),
            get_i8n_text('currency', user_filters.lang),
        ))

    if user_filters.min_usable_area:
        messages.append('{0}: `{1} {2}`'.format(
            get_i8n_text('filters.name.min_usable_area', user_filters.lang),
            user_filters.min_usable_area,
            get_i8n_text('filters.description.area_currency', user_filters.lang),
        ))

    if user_filters.layouts:
        layouts = [
            '`{0}`'.format(
                get_i8n_text('filters.button.layout.{0}.disabled'.format(layout_name), user_filters.lang),
            )
            for layout_name in user_filters.layouts
            if layout_name in app_settings.ENABLED_LAYOUTS
        ]
        messages.append('{0}: {1}'.format(
            get_i8n_text('filters.name.layout', user_filters.lang),
            ', '.join(layouts),
        ))
    else:
        messages.append('{0}: `{1}`'.format(
            get_i8n_text('filters.name.layout', user_filters.lang),
            get_i8n_text('filters.button.layout.all.disabled', user_filters.lang),
        ))

    if user_filters.districts:
        districts = [
            '`{0}`'.format(
                get_i8n_text('filters.button.district.number.disabled', user_filters.lang).format(district_number),
            )
            for district_number in user_filters.districts
            if district_number in app_settings.ENABLED_DISTRICTS
        ]
        messages.append('{0}: {1}'.format(
            get_i8n_text('filters.name.district', user_filters.lang),
            ', '.join(districts),
        ))
    else:
        messages.append('{0}: `{1}`'.format(
            get_i8n_text('filters.name.district', user_filters.lang),
            get_i8n_text('filters.button.district.all.disabled', user_filters.lang),
        ))

    return '\n'.join(messages)


def get_estate_post_settings(ads_for_post: Estate, lang: str) -> dict[str, Any]:
    """Set up estate message settings."""
    ads_link_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Go to advertisement', url=ads_for_post.page_url)],
        ],
        resize_keyboard=True,
    )
    return {
        'caption': _get_estate_description(ads_for_post, lang),
        'photo': ads_for_post.image_url,
        'parse_mode': 'Markdown',
        'reply_markup': ads_link_btn,
    }


def _get_estate_description(ads: Estate, lang: str) -> str:
    """Create a post for the bot."""
    output_messages = [
        get_i8n_text('ads.title.{0}.{1}'.format(
            ads.property_type,
            ads.category,
        ), lang),

        _get_link_without_quote(ads.address, ads.page_url),

        markdown.bold(
            '{0} {1}'.format(
                get_price_human_value(ads.price, lang),
                get_i8n_text('currency', lang),
            ),
        ),
    ]

    if ads.category == 'sale':
        output_messages.append(
            markdown.text(
                '{0} {1}/{2}'.format(
                    get_price_human_value(ads.price // ads.usable_area, lang),
                    get_i8n_text('currency', lang),
                    get_i8n_text('filters.description.area_currency', lang),
                ),
            ),
        )

    output_messages.append(
        markdown.text('{0} {1}, {2}'.format(
            ads.usable_area,
            get_i8n_text('filters.description.area_currency', lang),
            get_i8n_text('filters.button.layout.{0}.disabled'.format(ads.layout), lang),
        )),
    )

    if len(ads.energy_rating) == 1:
        output_messages.append(
            markdown.text(get_i8n_text('ads.energy_rate', lang).format(
                ads.energy_rating.upper(),
            )),
        )

    source_slug = 'ads.source.duplicate' if ads.is_duplicate else 'ads.source.new'
    output_messages.append(
        markdown.text(get_i8n_text(source_slug, lang).format(
            _get_link_without_quote(
                _get_source_name_link(ads.source_name),
                ads.page_url,
            ),
        )),
    )
    return markdown.text(*output_messages, sep='\n')


def get_price_human_value(price: int | None, lang: str) -> str:
    """Return human-friendly price string."""
    if not price or price < 0:
        return get_i8n_text('filters.description.price_not_set', lang)
    return '{0:,}'.format(price).replace(',', ' ')  # noqa: C819


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
    return mapa.get(source_name, 'other')


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
