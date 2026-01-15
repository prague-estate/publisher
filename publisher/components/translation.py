"""Bot i8n."""

_i8n = {
    'start.set_filters': {
        'en': '🏠 Set your filters and receive new rental or sale ads from all over Prague in one place.',
        'ru': '🏠 Настрой фильтры и получай новые объявления о недвижимости со всей Праги в одном месте.',
    },
    'start.subscribe_first': {
        'en': '🏠 Welcome to PragueEstate bot!\nPlease, subscribe first! 🔴 ⬇\n😎 First week is for free!',
        'ru': '🏠 Добро пожаловать в PragueEstate bot!\nПожалуйста, оформите подписку! 🔴 ⬇\n😎 Первая неделя бесплатно!',
    },
    'notify.disabled': {
        'en': "We'll stop bothering you with notices.\nWe hope you've found your dream home! 🏠",
        'ru': 'Мы больше не будем вас беспокоить уведомлениями.\nНадеемся, Вы нашли жилье своей мечты! 🏠',
    },
    'notify.enabled': {
        'en': "We'll send you new ads as soon as they're posted!\nBased on your filters:\n\n{0}",
        'ru': 'Мы пришлем вам новые объявления, как только они будут опубликованы!\nС учётем ваших предпочтений:\n\n{0}',
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
    'menu.admin': {'en': 'staff only', 'ru': 'служебное меню'},
    'menu.notify.inactive': {'en': '🔴 Notifications', 'ru': '🔴 Уведомления'},
    'menu.notify.active': {'en': '🟢 Notifications', 'ru': '🟢 Уведомления'},
    'menu.lang.en': {'en': '🇬🇧 Language', 'ru': '🇬🇧 Language'},
    'menu.lang.ru': {'en': '🇷🇺 Язык', 'ru': '🇷🇺 Язык'},
    'menu.lang.cz': {'en': 'Jazyk', 'ru': '🇨🇿 Jazyk'},
    'currency': {'en': 'Kč', 'ru': 'Kč'},
    'about': {
        'en': 'Hello and welcome!\nHere is a bot that can check for you if there are new ads to find a flat in Prague. According to your preferences. To rent or to buy.\n\nTo keep an eye on all the ads, join these channels:\n@prague_estate_rent\n@prague_estate_sale\n\nFor any questions and bugs write direct to @esemiko',
        'ru': 'Привет и добро пожаловать!\nЭтот бот может проверяет за вас нет ли новых объявлений о недвижимости в Праге. Соотвестенно вашим предпочтениям. Для аренды или покупки.\n\nЧтобы следить за всеми объявлениями, присоединяйтесь к каналам:\n@prague_estate_rent\n@prague_estate_sale\n\nПо всем вопросам и багам пишите @esemiko',
    },
    'estates.example': {
        'en': "⬆️ Here's the latest advert for your criteria.",
        'ru': '⬆️ Вот последние объявления по вашим предпочтениям.',
    },
    'filters.set.enable_notifications': {
        'en': 'Filters are set!\nEnable notifications to receive new ads.',
        'ru': 'Фильтры заданы!\nВключите уведомления, чтобы получать новые объявления.',
    },
    'subscription.active': {
        'en': 'Your subscription active until {0}.\nChoose renew option below:',
        'ru': 'Ваша подписка активна до {0}.\nВыберите вариант продления ниже:',
    },
    'subscription.inactive': {
        'en': 'You have no active subscription yet!\nChoose payment option below:',
        'ru': 'У вас еще нет активной подписки!\nВыберите способ оплаты ниже:',
    },
    'subscription.expired': {
        'en': 'Your subscription will expire soon!\nYou can renew early below:',
        'ru': 'Ваша подписка скоро истечёт!\nВы можете продлить ее заранее:',
    },
    'subscription.downgraded': {
        'en': 'Your subscription was expired!\nChoose payment option below:',
        'ru': 'Ваша подписка истекла!\nВыберите способ оплаты ниже:',
    },
    'invoice.description': {
        'en': 'New estates notifications in your telegram. Fast as a shark 🦈',
        'ru': 'Уведомления о новых квартирах прямо в вашем телеграме. Быстрее конкурентов 🦈',
    },
    'invoice.expired': {'en': 'Invoice expired!', 'ru': 'Инвойс устарел!'},
    'invoice.invalid': {'en': 'Invoice invalid!', 'ru': 'Инвойс сломался!'},
    'payment.accepted': {
        'en': 'Your subscription has been extended until {0}!',
        'ru': 'Ваша подписка была успешно продлена до {0}!',
    },
    'trial': {'en': 'Free trial access (1 week)', 'ru': 'Пробный доступ на неделю'},
    'trial.already_used': {'en': 'Trial access was already used!', 'ru': 'Пробный доступ уже был использован!'},
    'settings.description': {'en': '⬇️Set up your bot settings.', 'ru': '⬇️Настройки поведения бота.'},
    'filters.description': {
        'en': '⬇️Set up your filters for notifications.',
        'ru': '⬇️Настройте фильтры поиска объектов недвижимости для уведомлений.',
    },
    'filters.description.category': {'en': 'Set the category:', 'ru': 'Выберите категорию объявления:'},
    'filters.description.property_type': {'en': 'Set the property type:', 'ru': 'Выберите тип объекта:'},
    'filters.description.min_price': {
        'en': 'Set the minimum price.\n\nCurrent threshold: {0}',
        'ru': 'Установите минимальную цену.\n\nТекущий порог: {0}',
    },
    'filters.description.min_price.input': {
        'en': 'Input the minimum price in Kč:',
        'ru': 'Введите минимальную цену в Kč:',
    },
    'filters.description.min_price.invalid': {
        'en': 'Input a value greater than zero or cancel by click "Back" button above.',
        'ru': 'Введите значение больше О или отмените ввод нажав "Назад".',
    },
    'filters.description.max_price': {
        'en': 'Set the highest price.\n\nCurrent threshold: {0}',
        'ru': 'Установите максимальную цену.\n\nТекущий порог: {0}',
    },
    'filters.description.max_price.input': {
        'en': 'Input the highest price in Kč:',
        'ru': 'Введите максимальную цену в Kč:',
    },
    'filters.description.max_price.invalid': {
        'en': 'Input a value greater than zero or cancel by click "Back" button above.',
        'ru': 'Введите значение больше О или отмените ввод нажав "Назад".',
    },
    'filters.description.layout': {'en': 'Select required layouts:', 'ru': 'Выберите желаемую планировку:'},
    'filters.description.district': {'en': 'Select required districts:', 'ru': 'Выберите желаемый район:'},
    'filters.button.back': {'en': '⬅️ Back', 'ru': '⬅️ Назад'},
    'filters.button.close': {'en': 'Close', 'ru': 'Закрыть'},
    'filters.button.category.enabled': {'en': 'Category ✅', 'ru': 'Категория ✅'},
    'filters.button.category.disabled': {'en': 'Category ⚙', 'ru': 'Категория ⚙'},
    'filters.button.category.all.enabled': {'en': '✅ All', 'ru': '✅ Все'},
    'filters.button.category.all.disabled': {'en': 'All', 'ru': 'Все'},
    'filters.button.category.sale.enabled': {'en': '✅ Sale', 'ru': '✅ Продажа'},
    'filters.button.category.sale.disabled': {'en': 'Sale', 'ru': 'Покупка'},
    'filters.button.category.lease.enabled': {'en': '✅ Rent', 'ru': '✅ Аренда'},
    'filters.button.category.lease.disabled': {'en': 'Rent', 'ru': 'Аренда'},
    'filters.button.property_type.enabled': {'en': 'Type ✅', 'ru': 'Тип ✅'},
    'filters.button.property_type.disabled': {'en': 'Type ⚙', 'ru': 'Тип ⚙'},
    'filters.button.property_type.all.enabled': {'en': '✅ All', 'ru': '✅ Все'},
    'filters.button.property_type.all.disabled': {'en': 'All', 'ru': 'Все'},
    'filters.button.property_type.house.enabled': {'en': '✅ House', 'ru': '✅ Дом'},
    'filters.button.property_type.house.disabled': {'en': 'House', 'ru': 'Дом'},
    'filters.button.property_type.flat.enabled': {'en': '✅ Flat', 'ru': '✅ Квартира'},
    'filters.button.property_type.flat.disabled': {'en': 'Flat', 'ru': 'Квартира'},
    'filters.button.min_price.enabled': {'en': 'Min price ✅', 'ru': 'Мин цена ✅'},
    'filters.button.min_price.disabled': {'en': 'Min price ⚙', 'ru': 'Мин цена ⚙'},
    'filters.button.min_price.all.enabled': {'en': '✅ All', 'ru': '✅ Все'},
    'filters.button.min_price.all.disabled': {'en': 'All', 'ru': 'Все'},
    'filters.button.min_price.custom.enabled': {'en': '✅ Custom', 'ru': '✅ Заданная'},
    'filters.button.min_price.custom.disabled': {'en': 'Custom', 'ru': 'Заданная'},
    'filters.button.max_price.enabled': {'en': 'Max price ✅', 'ru': 'Макс цена ✅'},
    'filters.button.max_price.disabled': {'en': 'Max price ⚙', 'ru': 'Макс цена ⚙'},
    'filters.button.max_price.all.enabled': {'en': '✅ All', 'ru': '✅ Все'},
    'filters.button.max_price.all.disabled': {'en': 'All', 'ru': 'Все'},
    'filters.button.max_price.custom.enabled': {'en': '✅ Custom', 'ru': '✅ Заданная'},
    'filters.button.max_price.custom.disabled': {'en': 'Custom', 'ru': 'Заданная'},
    'filters.button.layout.enabled': {'en': 'Layout ✅', 'ru': 'Планировка ✅'},
    'filters.button.layout.disabled': {'en': 'Layout ⚙', 'ru': 'Планировка ⚙'},
    'filters.button.layout.all.enabled': {'en': '✅ All', 'ru': '✅ Все'},
    'filters.button.layout.all.disabled': {'en': 'All', 'ru': 'Все'},
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
    'filters.button.layout.four_more.enabled': {'en': '✅ 5 and more', 'ru': '✅ 5 и больше'},
    'filters.button.layout.four_more.disabled': {'en': '5 and more', 'ru': '5 и больше'},
    'filters.button.layout.others.enabled': {'en': '✅ others', 'ru': '✅ другие'},
    'filters.button.layout.others.disabled': {'en': 'others', 'ru': 'другие'},
    'filters.button.district.enabled': {'en': 'District ✅', 'ru': 'Район ✅'},
    'filters.button.district.disabled': {'en': 'District ⚙', 'ru': 'Район ⚙'},
    'filters.button.district.all.enabled': {'en': '✅ All', 'ru': '✅ Все'},
    'filters.button.district.all.disabled': {'en': 'All', 'ru': 'Все'},
    'filters.button.district.number.enabled': {'en': '✅ Praha {0}', 'ru': '✅ Прага {0}'},
    'filters.button.district.number.disabled': {'en': 'Praha {0}', 'ru': 'Прага {0}'},

    'price.week': {'en': 'Week access', 'ru': 'Неделя доступа'},
    'price.month': {'en': 'Month access 🌟', 'ru': 'Месяц доступа 🌟'},
    'price.year': {'en': 'Year access', 'ru': 'Год доступа'},
    'price.test': {'en': 'Test access', 'ru': 'Тестовый доступ'},
}


def get_i8n_text(slug: str, lang: str) -> str:
    """Return translated message."""
    return _i8n[slug][lang]


def get_by(slug: str) -> set[str]:
    """Return translations."""
    return set(_i8n[slug].values())
