"""Bot texts."""

_bot_messages: dict[str, str] = {
    'start.set_filters': '🏠 Set your filters and receive new rental or sale ads from all over Prague in one place.',
    'start.subscribe_first': '🏠 Welcome to PragueEstate bot!\n      Please, subscribe first! 🔴 ⬇️\n😎 First week is for free!',

    'notify.disabled': "We'll stop bothering you with notices.\n We hope you've found your dream home! 🏠",
    'notify.enabled': "We'll send you new ads as soon as they're posted!\nBased on your filters:\n\n{0}",

    'menu.subscription.inactive': '🔴 Subscribe',
    'menu.subscription.active': '🟢 Subscription',
    'menu.about': 'About',
    'menu.filters': 'Filters',
    'menu.admin': 'staff only',
    'menu.notify.inactive': '🔴 Notify',
    'menu.notify.active': '🟢 Notify',

    'currency': 'Kč',

    'about': """Hello and welcome!
Here is a bot that can check for you if there are new ads to find a flat in Prague. To rent or to buy.

It's gonna look in here:
sreality.cz
bezrealitky.cz
svoboda-williams.com
expats.cz
reality.idnes.cz
engelvoelkers.com
remax-czech.cz

For any questions and bugs write direct to @esemiko""",

    'estates.example': "⬆️ Here's the latest advert for your criteria.",

    'filters.set.enable_notifications': 'Filters are set!\nEnable notifications to receive new ads.',

    'subscription.active': 'Your subscription active until {0}.\nChoose renew option below:',
    'subscription.inactive': 'You have no active subscription yet!\nChoose payment option below:',
    'subscription.expired': 'Your subscription will expire soon!\nYou can renew early below:',
    'subscription.downgraded': 'Your subscription was expired!\nChoose payment option below:',

    'invoice.description': 'New estates notifications in your telegram. Fast as a shark 🦈',
    'invoice.expired': 'Invoice expired!',
    'invoice.invalid': 'Invoice invalid!',
    'payment.accepted': 'Your subscription has been extended until {0}!',
    'trial': 'Free trial access (1 week)',
    'trial.already_used': 'Trial access was already used!',

    'filters.description': '⬇️ Set up your filters for notifications.',
    'filters.description.category': 'Set the category:',
    'filters.description.max_price': 'Set the highest price.\n\nCurrent threshold: {0}',
    'filters.description.max_price.input': 'Input the highest price in Kč:',
    'filters.description.max_price.invalid': 'Input a value greater than zero or cancel by click "Back" button above.',
    'filters.description.layout': 'Select required layouts:',
    'filters.description.district': 'Select required districts:',

    'filters.button.back': '⬅️ Back',
    'filters.button.close': 'Close',

    'filters.button.category.enabled': 'Category ✅',
    'filters.button.category.disabled': 'Category ⚙',
    'filters.button.category.all.enabled': '✅ All',
    'filters.button.category.all.disabled': 'All',
    'filters.button.category.sale.enabled': '✅ Sale',
    'filters.button.category.sale.disabled': 'Sale',
    'filters.button.category.lease.enabled': '✅ Rent',
    'filters.button.category.lease.disabled': 'Rent',

    'filters.button.max_price.enabled': 'Max price ✅',
    'filters.button.max_price.disabled': 'Max price ⚙',
    'filters.button.max_price.all.enabled': '✅ All',
    'filters.button.max_price.all.disabled': 'All',
    'filters.button.max_price.custom.enabled': '✅ Custom',
    'filters.button.max_price.custom.disabled': 'Custom',

    'filters.button.layout.enabled': 'Layout ✅',
    'filters.button.layout.disabled': 'Layout ⚙',
    'filters.button.layout.all.enabled': '✅ All',
    'filters.button.layout.all.disabled': 'All',
    'filters.button.layout.one_kk.enabled': '✅ 1+kk',
    'filters.button.layout.one_kk.disabled': '1+kk',
    'filters.button.layout.one_one.enabled': '✅ 1+1',
    'filters.button.layout.one_one.disabled': '1+1',
    'filters.button.layout.two_kk.enabled': '✅ 2+kk',
    'filters.button.layout.two_kk.disabled': '2+kk',
    'filters.button.layout.two_one.enabled': '✅ 2+1',
    'filters.button.layout.two_one.disabled': '2+1',
    'filters.button.layout.three_kk.enabled': '✅ 3+kk',
    'filters.button.layout.three_kk.disabled': '3+kk',
    'filters.button.layout.three_one.enabled': '✅ 3+1',
    'filters.button.layout.three_one.disabled': '3+1',
    'filters.button.layout.four_kk.enabled': '✅ 4+kk',
    'filters.button.layout.four_kk.disabled': '4+kk',
    'filters.button.layout.four_more.enabled': '✅ 5 and more',
    'filters.button.layout.four_more.disabled': '5 and more',
    'filters.button.layout.others.enabled': '✅ others',
    'filters.button.layout.others.disabled': 'others',

    'filters.button.district.enabled': 'District ✅',
    'filters.button.district.disabled': 'District ⚙',
    'filters.button.district.all.enabled': '✅ All',
    'filters.button.district.all.disabled': 'All',
    'filters.button.district.number.enabled': '✅ Praha {0}',
    'filters.button.district.number.disabled': 'Praha {0}',
}


def get_message(slug: str) -> str:
    """Return message by placeholder."""
    return _bot_messages[slug]
