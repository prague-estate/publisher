"""Bot texts."""

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
    'trial': 'Free trial access',
    'trial.already_used': 'Trial access was already used!',

    'filters.description': 'Set up your estate objects filters for automatic notifications.',
    'filters.description.category': 'Set specified category for search',
    'filters.description.max_price': 'Set maximum price of estate.\n\nCurrent threshold: {0} Kč',
    'filters.description.max_price.input': 'Input maximum price of searched estate in Kč',
    'filters.description.max_price.invalid': 'Input positive number or cancel by click "Back" button above',

    'filters.button': 'Filters',

    'filters.button.notifications.enabled': 'Notifications: ✅',
    'filters.button.notifications.disabled': 'Notifications: ⏸',

    'filters.button.category': 'Category ⚙',
    'filters.button.category.all.enabled': '✅All',
    'filters.button.category.all.disabled': 'All',
    'filters.button.category.sale.enabled': '✅Sale',
    'filters.button.category.sale.disabled': 'Sale',
    'filters.button.category.lease.enabled': '✅Rent',
    'filters.button.category.lease.disabled': 'Rent',

    'filters.button.max_price': 'Max price ⚙',
    'filters.button.max_price.all.enabled': '✅All',
    'filters.button.max_price.all.disabled': 'All',
    'filters.button.max_price.custom.enabled': '✅Custom',
    'filters.button.max_price.custom.disabled': 'Custom',

    'filters.button.back': '⬅Back',
}


def get_message(slug: str) -> str:
    """Return message by placeholder."""
    return _bot_messages[slug]
