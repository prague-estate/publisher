"""Bot i8n."""

_i8n = {
    'start.set_filters': {
        'en': '🏠 Set your filters and receive new rental or sale ads from all over Prague in one place.',
        'ru': '🏠 Set your filters and receive new rental or sale ads from all over Prague in one place.',
    },
    'start.subscribe_first': {
        'en': '🏠 Welcome to PragueEstate bot!\n      Please, subscribe first! 🔴 ⬇️\n😎 First week is for free!',
        'ru': '🏠 Welcome to PragueEstate bot!\n      Please, subscribe first! 🔴 ⬇️\n😎 First week is for free!',
    },
    'notify.disabled': {
        'en': "We'll stop bothering you with notices.\nWe hope you've found your dream home! 🏠",
        'ru': "We'll stop bothering you with notices.\nWe hope you've found your dream home! 🏠",
    },
    'notify.enabled': {
        'en': "We'll send you new ads as soon as they're posted!\nBased on your filters:\n\n{0}",
        'ru': "We'll send you new ads as soon as they're posted!\nBased on your filters:\n\n{0}",
    },
    'settings.updated': {
        'en': 'New settings applied',
        'ru': 'Новые настройки применены',
    },

    'menu.subscription.inactive': {
        'en': '🔴 Subscribe',
        'ru': '🔴 Подпишись',
    },
    'menu.subscription.active': {
        'en': '🟢 Subscription',
        'ru': '🟢 Подписка',
    },

    'menu.about': {'en': 'ℹ️ About', 'ru': 'ℹ️ О проекте'},
    'menu.filters': {'en': '🔍 Filters', 'ru': '🔍 Фильтры'},
    'menu.settings': {'en': '⚙ Settings', 'ru': '⚙ Настройки'},
    'menu.admin': {'en': 'staff only', 'ru': 'staff only'},
    'menu.notify.inactive': {'en': '🔴 Notifications', 'ru': '🔴 Уведомления'},
    'menu.notify.active': {'en': '🟢 Notifications', 'ru': '🟢 Уведомления'},
    'menu.lang.en': {'en': '🇬🇧 Language', 'ru': '🇬🇧 Language'},
    'menu.lang.ru': {'en': '🇷🇺 Язык', 'ru': '🇷🇺 Язык'},
    'menu.lang.cz': {'en': 'Unknown', 'ru': 'Unknown'},
    'currency': {'en': 'Kč', 'ru': 'Kč'},
    'about': {
        'en': 'Hello and welcome!\nHere is a bot that can check for you if there are new ads to find a flat in Prague. According to your preferences. To rent or to buy.\n\nTo keep an eye on all the ads, join these channels:\n@prague_estate_rent\n@prague_estate_sale\n\nFor any questions and bugs write direct to @esemiko',
        'ru': 'Hello and welcome!\nHere is a bot that can check for you if there are new ads to find a flat in Prague. According to your preferences. To rent or to buy.\n\nTo keep an eye on all the ads, join these channels:\n@prague_estate_rent\n@prague_estate_sale\n\nFor any questions and bugs write direct to @esemiko',
    },
    'estates.example': {
        'en': "⬆️ Here's the latest advert for your criteria.",
        'ru': "⬆️ Here's the latest advert for your criteria.",
    },
    'filters.set.enable_notifications': {
        'en': 'Filters are set!\nEnable notifications to receive new ads.',
        'ru': 'Filters are set!\nEnable notifications to receive new ads.',
    },
    'subscription.active': {
        'en': 'Your subscription active until {0}.\nChoose renew option below:',
        'ru': 'Your subscription active until {0}.\nChoose renew option below:',
    },
    'subscription.inactive': {
        'en': 'You have no active subscription yet!\nChoose payment option below:',
        'ru': 'You have no active subscription yet!\nChoose payment option below:',
    },
    'subscription.expired': {
        'en': 'Your subscription will expire soon!\nYou can renew early below:',
        'ru': 'Your subscription will expire soon!\nYou can renew early below:',
    },
    'subscription.downgraded': {
        'en': 'Your subscription was expired!\nChoose payment option below:',
        'ru': 'Your subscription was expired!\nChoose payment option below:',
    },
    'invoice.description': {
        'en': 'New estates notifications in your telegram. Fast as a shark 🦈',
        'ru': 'New estates notifications in your telegram. Fast as a shark 🦈',
    },
    'invoice.expired': {'en': 'Invoice expired!', 'ru': 'Invoice expired!'},
    'invoice.invalid': {'en': 'Invoice invalid!', 'ru': 'Invoice invalid!'},
    'payment.accepted': {
        'en': 'Your subscription has been extended until {0}!',
        'ru': 'Your subscription has been extended until {0}!',
    },
    'trial': {'en': 'Free trial access (1 week)', 'ru': 'Free trial access (1 week)'},
    'trial.already_used': {'en': 'Trial access was already used!', 'ru': 'Trial access was already used!'},
    'settings.description': {'en': '⬇️ Set up your bot settings.', 'ru': '⬇️ Set up your bot settings.'},
    'filters.description': {
        'en': '⬇️ Set up your filters for notifications.',
        'ru': '⬇️ Set up your filters for notifications.',
    },
    'filters.description.category': {'en': 'Set the category:', 'ru': 'Set the category:'},
    'filters.description.property_type': {'en': 'Set the property type:', 'ru': 'Set the property type:'},
    'filters.description.min_price': {
        'en': 'Set the minimum price.\n\nCurrent threshold: {0}',
        'ru': 'Set the minimum price.\n\nCurrent threshold: {0}',
    },
    'filters.description.min_price.input': {
        'en': 'Input the minimum price in Kč:',
        'ru': 'Input the minimum price in Kč:',
    },
    'filters.description.min_price.invalid': {
        'en': 'Input a value greater than zero or cancel by click "Back" button above.',
        'ru': 'Input a value greater than zero or cancel by click "Back" button above.',
    },
    'filters.description.max_price': {
        'en': 'Set the highest price.\n\nCurrent threshold: {0}',
        'ru': 'Set the highest price.\n\nCurrent threshold: {0}',
    },
    'filters.description.max_price.input': {
        'en': 'Input the highest price in Kč:',
        'ru': 'Input the highest price in Kč:',
    },
    'filters.description.max_price.invalid': {
        'en': 'Input a value greater than zero or cancel by click "Back" button above.',
        'ru': 'Input a value greater than zero or cancel by click "Back" button above.',
    },
    'filters.description.layout': {'en': 'Select required layouts:', 'ru': 'Select required layouts:'},
    'filters.description.district': {'en': 'Select required districts:', 'ru': 'Select required districts:'},
    'filters.button.back': {'en': '⬅️ Back', 'ru': '⬅️ Back'},
    'filters.button.close': {'en': 'Close', 'ru': 'Close'},
    'filters.button.category.enabled': {'en': 'Category ✅', 'ru': 'Category ✅'},
    'filters.button.category.disabled': {'en': 'Category ⚙', 'ru': 'Category ⚙'},
    'filters.button.category.all.enabled': {'en': '✅ All', 'ru': '✅ All'},
    'filters.button.category.all.disabled': {'en': 'All', 'ru': 'All'},
    'filters.button.category.sale.enabled': {'en': '✅ Sale', 'ru': '✅ Sale'},
    'filters.button.category.sale.disabled': {'en': 'Sale', 'ru': 'Sale'},
    'filters.button.category.lease.enabled': {'en': '✅ Rent', 'ru': '✅ Rent'},
    'filters.button.category.lease.disabled': {'en': 'Rent', 'ru': 'Rent'},
    'filters.button.property_type.enabled': {'en': 'Type ✅', 'ru': 'Type ✅'},
    'filters.button.property_type.disabled': {'en': 'Type ⚙', 'ru': 'Type ⚙'},
    'filters.button.property_type.all.enabled': {'en': '✅ All', 'ru': '✅ All'},
    'filters.button.property_type.all.disabled': {'en': 'All', 'ru': 'All'},
    'filters.button.property_type.house.enabled': {'en': '✅ House', 'ru': '✅ House'},
    'filters.button.property_type.house.disabled': {'en': 'House', 'ru': 'House'},
    'filters.button.property_type.flat.enabled': {'en': '✅ Flat', 'ru': '✅ Flat'},
    'filters.button.property_type.flat.disabled': {'en': 'Flat', 'ru': 'Flat'},
    'filters.button.min_price.enabled': {'en': 'Min price ✅', 'ru': 'Min price ✅'},
    'filters.button.min_price.disabled': {'en': 'Min price ⚙', 'ru': 'Min price ⚙'},
    'filters.button.min_price.all.enabled': {'en': '✅ All', 'ru': '✅ All'},
    'filters.button.min_price.all.disabled': {'en': 'All', 'ru': 'All'},
    'filters.button.min_price.custom.enabled': {'en': '✅ Custom', 'ru': '✅ Custom'},
    'filters.button.min_price.custom.disabled': {'en': 'Custom', 'ru': 'Custom'},
    'filters.button.max_price.enabled': {'en': 'Max price ✅', 'ru': 'Max price ✅'},
    'filters.button.max_price.disabled': {'en': 'Max price ⚙', 'ru': 'Max price ⚙'},
    'filters.button.max_price.all.enabled': {'en': '✅ All', 'ru': '✅ All'},
    'filters.button.max_price.all.disabled': {'en': 'All', 'ru': 'All'},
    'filters.button.max_price.custom.enabled': {'en': '✅ Custom', 'ru': '✅ Custom'},
    'filters.button.max_price.custom.disabled': {'en': 'Custom', 'ru': 'Custom'},
    'filters.button.layout.enabled': {'en': 'Layout ✅', 'ru': 'Layout ✅'},
    'filters.button.layout.disabled': {'en': 'Layout ⚙', 'ru': 'Layout ⚙'},
    'filters.button.layout.all.enabled': {'en': '✅ All', 'ru': '✅ All'},
    'filters.button.layout.all.disabled': {'en': 'All', 'ru': 'All'},
    'filters.button.layout.one_kk.enabled': {'en': '✅ 1+kk', 'ru': '✅ 1+kk'},
    'filters.button.layout.one_kk.disabled': {'en': '1+kk', 'ru': '1+kk'},
    'filters.button.layout.one_one.enabled': {'en': '✅ 1+1', 'ru': '✅ 1+1'},
    'filters.button.layout.one_one.disabled': {'en': '1+1', 'ru': '1+1'},
    'filters.button.layout.two_kk.enabled': {'en': '✅ 2+kk', 'ru': '✅ 2+kk'},
    'filters.button.layout.two_kk.disabled': {'en': '2+kk', 'ru': '2+kk'},
    'filters.button.layout.two_one.enabled': {'en': '✅ 2+1', 'ru': '✅ 2+1'},
    'filters.button.layout.two_one.disabled': {'en': '2+1', 'ru': '2+1'},
    'filters.button.layout.three_kk.enabled': {'en': '✅ 3+kk', 'ru': '✅ 3+kk'},
    'filters.button.layout.three_kk.disabled': {'en': '3+kk', 'ru': '3+kk'},
    'filters.button.layout.three_one.enabled': {'en': '✅ 3+1', 'ru': '✅ 3+1'},
    'filters.button.layout.three_one.disabled': {'en': '3+1', 'ru': '3+1'},
    'filters.button.layout.four_kk.enabled': {'en': '✅ 4+kk', 'ru': '✅ 4+kk'},
    'filters.button.layout.four_kk.disabled': {'en': '4+kk', 'ru': '4+kk'},
    'filters.button.layout.four_more.enabled': {'en': '✅ 5 and more', 'ru': '✅ 5 and more'},
    'filters.button.layout.four_more.disabled': {'en': '5 and more', 'ru': '5 and more'},
    'filters.button.layout.others.enabled': {'en': '✅ others', 'ru': '✅ others'},
    'filters.button.layout.others.disabled': {'en': 'others', 'ru': 'others'},
    'filters.button.district.enabled': {'en': 'District ✅', 'ru': 'District ✅'},
    'filters.button.district.disabled': {'en': 'District ⚙', 'ru': 'District ⚙'},
    'filters.button.district.all.enabled': {'en': '✅ All', 'ru': '✅ All'},
    'filters.button.district.all.disabled': {'en': 'All', 'ru': 'All'},
    'filters.button.district.number.enabled': {'en': '✅ Praha {0}', 'ru': '✅ Praha {0}'},
    'filters.button.district.number.disabled': {'en': 'Praha {0}', 'ru': 'Praha {0}'},
}


# fixme remove usage
def get_message(slug: str) -> str:
    """Return en message by slug."""
    return get_i8n_text(slug, 'en')


def get_i8n_text(slug: str, lang: str) -> str:
    """Return translated message."""
    return _i8n[slug][lang]


def get_by(slug: str) -> set[str]:
    """Return translations."""
    return set(_i8n[slug].values())
