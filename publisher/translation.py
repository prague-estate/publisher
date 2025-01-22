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
    'filters.description.category': 'Select search category',

    'filters.button': 'Filters',

    'filters.button.notifications.enabled': 'Notifications: ✅',
    'filters.button.notifications.disabled': 'Notifications: ⏸',

    'filters.button.category': 'Category ⚙',
    'filters.button.category.sale.enabled': '✅Sale',
    'filters.button.category.sale.disabled': 'Sale',
    'filters.button.category.rent.enabled': '✅Rent',
    'filters.button.category.rent.disabled': 'Rent',

    'filters.button.reset': '🔄Reset',
    'filters.button.back': '⬅Back',
}


def get_message(slug: str) -> str:
    """Return message by placeholder."""
    return _bot_messages[slug]
