"""Telegram bot handlers."""
import asyncio
import logging
from itertools import cycle

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery
from aiogram.utils.deep_linking import create_start_link

from publisher.components import api_client, presenter, storage, translation, types
from publisher.settings import app_settings, prices_settings

logger = logging.getLogger(__file__)

bot_instance = Bot(app_settings.BOT_TOKEN)
dp = Dispatcher(storage=RedisStorage.from_url(app_settings.REDIS_DSN))


class Form(StatesGroup):
    """Change filters states."""

    max_price = State()
    min_price = State()


@dp.message(CommandStart(deep_link=True))
@dp.message(Command('start'))
async def start(message: Message, command: CommandObject) -> None:
    """Apply promo trial if exists."""
    promo = str(command.args).strip().lower()
    logger.info(f'Start {promo=}')
    promo_days: int | None = app_settings.PROMO_CODES.get(promo)

    if message.from_user and message.from_user.language_code in app_settings.ENABLED_LANGUAGES:
        lang = message.from_user.language_code
    else:
        lang = app_settings.ENABLED_LANGUAGES[0]
    logger.info('set user lang to {0} {1}'.format(
        message.from_user,
        lang,
    ))
    storage.update_user_settings(user_id=message.chat.id, lang=lang)

    if promo_days and not storage.has_used_trial(message.chat.id, promo):
        logger.info('apply promo code')
        sub = storage.renew_subscription(
            user_id=message.chat.id,
            days=promo_days,
        )
        storage.mark_used_trial(message.chat.id, promo)

        await message.answer(  # type: ignore
            text=translation.get_i8n_text('payment.accepted', lang).format(sub.expired_at.isoformat()),
        )

    actual_sub = storage.get_subscription(message.chat.id)
    if actual_sub and actual_sub.is_active:
        await message.answer(  # type: ignore
            text=translation.get_i8n_text('start.set_filters', lang),
            reply_markup=presenter.get_main_menu(message.chat.id),
        )

    else:
        await message.answer(  # type: ignore
            text=translation.get_i8n_text('start.subscribe_first', lang),
            reply_markup=presenter.get_main_menu(message.chat.id),
        )


@dp.message(Command('support'))
@dp.message(Command('paysupport'))
@dp.message(F.text.in_(translation.get_by('menu.about')))
async def about(message: Message) -> None:
    """About project."""
    logger.info('About')
    await message.answer(
        text=translation.get_message('about'),
        reply_markup=presenter.get_main_menu(message.chat.id),
    )


@dp.message(F.text.in_(translation.get_by('menu.admin')))
async def admin_info(message: Message) -> None:
    """Show info for admins."""
    logger.info('Admin info')

    if not app_settings.is_admin(message.chat.id):
        logger.error('not by admin request!')
        return

    response_messages = [
        'Available promo links',
    ]

    response_messages += [
        '[{0}]({1}) for {2} days'.format(
            code,
            await create_start_link(bot_instance, code),
            days,
        )
        for code, days in app_settings.PROMO_CODES.items()
    ]

    response_messages += [
        '',
        'Active subs: {0}'.format(len(storage.get_active_subscriptions())),
    ]

    await message.answer(
        text='\n'.join(response_messages),
        reply_markup=presenter.get_main_menu(message.chat.id),
        parse_mode='Markdown',
    )


@dp.message(F.text.in_(
    translation.get_by('menu.subscription.inactive') | translation.get_by('menu.subscription.active'),
))
async def user_subscription(message: Message) -> None:
    """Subscription info."""
    logger.info('Subscription')

    sub = storage.get_subscription(message.chat.id)
    if sub and sub.is_active:
        text = translation.get_message('subscription.active').format(sub.expired_at.isoformat())
    else:
        text = translation.get_message('subscription.inactive')

    await message.answer(
        text=text,
        reply_markup=presenter.get_prices_menu(message.chat.id),
    )


@dp.message(F.text.in_(translation.get_by('menu.filters')))
async def user_filters(message: Message) -> None:
    """User filters setup."""
    logger.info('User filters')

    await message.answer(
        text=translation.get_message('filters.description'),
        reply_markup=presenter.get_filters_menu(message.chat.id),
    )


@dp.message(F.text.in_(translation.get_by('menu.settings')))
async def user_settings(message: Message) -> None:
    """User settings setup."""
    logger.info('User settings')
    await message.answer(
        text=translation.get_message('settings.description'),
        reply_markup=presenter.get_settings_menu(message.chat.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:back')
async def filter_go_back(query: CallbackQuery, state: FSMContext | None = None) -> None:
    """Go back to filters."""
    logger.info('filter_go_back')

    if state:
        await state.clear()

    await query.message.edit_text(  # type: ignore
        text=translation.get_message('filters.description'),
        reply_markup=presenter.get_filters_menu(query.from_user.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:close')
async def filter_close(query: CallbackQuery, state: FSMContext | None = None) -> None:
    """Close filters."""
    logger.info('filter_close')

    if state:
        await state.clear()

    await query.message.delete()  # type: ignore

    filters_config = storage.get_user_settings(query.from_user.id)
    logger.info(f'filter_close {filters_config=}')
    if not filters_config.is_enabled_notifications:
        await query.message.answer(  # type: ignore
            text=translation.get_message('filters.set.enable_notifications'),
            reply_markup=presenter.get_main_menu(query.from_user.id),
        )
        return

    sub = storage.get_subscription(query.from_user.id)
    logger.info(f'filter_close {sub=}')
    if sub and sub.is_active:
        await _show_last_estate(filters_config, query.message)  # type: ignore

    await query.message.answer(  # type: ignore
        text=translation.get_message('notify.enabled').format(
            presenter.get_filters_representation(filters_config),
        ),
        reply_markup=presenter.get_main_menu(query.from_user.id),
        parse_mode='Markdown',
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'settings:toggle:enabled')
async def user_settings_toggle_notifications(query: CallbackQuery) -> None:
    """Change notifications status."""
    logger.info('notifications toggle')

    settings = storage.get_user_settings(query.from_user.id)
    if settings.is_enabled_notifications:
        storage.update_user_settings(query.from_user.id, enabled=False)
    else:
        storage.update_user_settings(query.from_user.id, enabled=True)

    await query.message.edit_reply_markup(  # type: ignore
        reply_markup=presenter.get_settings_menu(query.from_user.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'settings:toggle:lang')
async def user_settings_toggle_lang(query: CallbackQuery) -> None:
    """Change user language."""
    logger.info('language toggle')

    settings = storage.get_user_settings(query.from_user.id)

    if settings.lang not in app_settings.ENABLED_LANGUAGES:
        storage.update_user_settings(query.from_user.id, lang=app_settings.ENABLED_LANGUAGES[0])
    else:
        langs_cycle = cycle(app_settings.ENABLED_LANGUAGES)
        while True:
            lang = next(langs_cycle)
            if lang == settings.lang:
                storage.update_user_settings(query.from_user.id, lang=next(langs_cycle))
                break

    await query.message.edit_reply_markup(  # type: ignore
        reply_markup=presenter.get_settings_menu(query.from_user.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'settings:close')
async def user_settings_close(query: CallbackQuery, state: FSMContext | None = None) -> None:
    """Close settings."""
    logger.info('settings_close')
    if state:
        await state.clear()

    await query.message.delete()  # type: ignore
    await query.message.answer(  # type: ignore
        text=translation.get_message('settings.updated'),
        reply_markup=presenter.get_main_menu(query.from_user.id),
        parse_mode='Markdown',
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:district:show')
async def filter_change_district(query: CallbackQuery) -> None:
    """Show change district."""
    logger.info('filter_change_district')
    await query.message.edit_text(  # type: ignore
        text=translation.get_message('filters.description.district'),
        reply_markup=presenter.get_filters_district_menu(query.from_user.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:district:reset')
@dp.callback_query(lambda callback: callback.data and callback.data.startswith('filters:district:switch:'))
async def filter_change_district_switch(query: CallbackQuery) -> None:  # noqa: WPS213
    """Process change district."""
    filters_config = storage.get_user_settings(query.from_user.id)
    logger.info(f'filter_change_district_switch {query.data=} {filters_config.districts=}')
    district_for_switch = query.data.split(':')[-1]  # type: ignore

    if district_for_switch == 'reset':
        logger.info('filter_change_district_switch: reset')
        if filters_config.districts is not None:
            storage.update_user_settings(user_id=query.from_user.id, districts=None)
            await filter_change_district(query)
        return None

    if not district_for_switch.isdigit() or int(district_for_switch) not in app_settings.ENABLED_DISTRICTS:
        logger.error('invalid district value got!')
        return None

    district_for_switch = int(district_for_switch)
    if filters_config.districts is None:
        logger.info('filter_change_district_switch: enable from not set')
        storage.update_user_settings(
            user_id=query.from_user.id,
            districts={district_for_switch},
        )
        return await filter_change_district(query)

    elif district_for_switch in filters_config.districts:
        new_value = (filters_config.districts - {district_for_switch}) or None
        logger.info(f'filter_change_district_switch: disable, {new_value=}')
        storage.update_user_settings(
            user_id=query.from_user.id,
            districts=new_value,
        )
        return await filter_change_district(query)

    new_value = filters_config.districts | {district_for_switch}
    logger.info(f'filter_change_district_switch: enable, {new_value=}')
    storage.update_user_settings(
        user_id=query.from_user.id,
        districts=new_value,
    )
    return await filter_change_district(query)


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:layout:show')
async def filter_change_layout(query: CallbackQuery) -> None:
    """Show change layout."""
    logger.info('filter_change_layout')
    await query.message.edit_text(  # type: ignore
        text=translation.get_message('filters.description.layout'),
        reply_markup=presenter.get_filters_layout_menu(query.from_user.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:layout:reset')
@dp.callback_query(lambda callback: callback.data and callback.data.startswith('filters:layout:switch:'))
async def filter_change_layout_switch(query: CallbackQuery) -> None:  # noqa: WPS213
    """Process change layout."""
    filters_config = storage.get_user_settings(query.from_user.id)
    logger.info(f'filter_change_layout_switch {query.data=} {filters_config.layouts=}')
    layout_for_switch: str = query.data.split(':')[-1]  # type: ignore

    if layout_for_switch == 'reset':
        logger.info('filter_change_layout_switch: reset')
        if filters_config.layouts is not None:
            storage.update_user_settings(user_id=query.from_user.id, layouts=None)
            await filter_change_layout(query)
        return None

    if layout_for_switch not in app_settings.ENABLED_LAYOUTS:
        logger.error('invalid layout value got!')
        return None

    if filters_config.layouts is None:
        logger.info('filter_change_layout_switch: enable from not set')
        storage.update_user_settings(
            user_id=query.from_user.id,
            layouts={layout_for_switch},
        )
        return await filter_change_layout(query)

    elif layout_for_switch in filters_config.layouts:
        new_value = (filters_config.layouts - {layout_for_switch}) or None
        logger.info(f'filter_change_layout_switch: disable, {new_value=}')
        storage.update_user_settings(
            user_id=query.from_user.id,
            layouts=new_value,
        )
        return await filter_change_layout(query)

    new_value = filters_config.layouts | {layout_for_switch}
    logger.info(f'filter_change_layout_switch: enable, {new_value=}')
    storage.update_user_settings(
        user_id=query.from_user.id,
        layouts=new_value,
    )
    return await filter_change_layout(query)


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:category:show')
async def filter_change_category(query: CallbackQuery) -> None:
    """Show change category."""
    logger.info('filter_change_category')
    await query.message.edit_text(  # type: ignore
        text=translation.get_message('filters.description.category'),
        reply_markup=presenter.get_filters_category_menu(query.from_user.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:category:lease')
@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:category:sale')
@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:category:reset')
async def filter_change_category_switch(query: CallbackQuery) -> None:
    """Process change category."""
    logger.info(f'filter_change_category_switch {query.data=}')
    category_for_enable: str = query.data.split(':')[-1]  # type: ignore
    filters_config = storage.get_user_settings(query.from_user.id)

    if category_for_enable == 'reset':
        logger.info('filter_change_category_switch: reset')
        if filters_config.category is not None:
            storage.update_user_settings(
                user_id=query.from_user.id,
                category=None,
                min_price=None,
                max_price=None,
            )
            return await filter_change_category(query)

    elif filters_config.category != category_for_enable:
        logger.info(f'filter_change_category_switch: enable {category_for_enable}')
        storage.update_user_settings(
            user_id=query.from_user.id,
            category=category_for_enable,
            min_price=None,
            max_price=None,
        )
        return await filter_change_category(query)


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:property_type:show')
async def filter_change_property_type(query: CallbackQuery) -> None:
    """Show change property_type."""
    logger.info('filter_change_property_type')
    await query.message.edit_text(  # type: ignore
        text=translation.get_message('filters.description.property_type'),
        reply_markup=presenter.get_filters_property_type_menu(query.from_user.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:property_type:flat')
@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:property_type:house')
@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:property_type:reset')
async def filter_change_property_type_switch(query: CallbackQuery) -> None:
    """Process change property_type."""
    logger.info(f'filter_change_property_type_switch {query.data=}')
    value_for_enable: str = query.data.split(':')[-1]  # type: ignore
    filters_config = storage.get_user_settings(query.from_user.id)

    if value_for_enable == 'reset':
        logger.info('filter_change_property_type_switch: reset')
        if filters_config.property_type is not None:
            storage.update_user_settings(
                user_id=query.from_user.id,
                property_type=None,
                layouts=None,
            )
            return await filter_change_property_type(query)

    elif filters_config.property_type != value_for_enable:
        logger.info(f'filter_change_property_type_switch: enable {value_for_enable}')
        storage.update_user_settings(
            user_id=query.from_user.id,
            property_type=value_for_enable,
            layouts=None,
        )
        return await filter_change_property_type(query)


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:min_price:show')
async def filter_change_min_price(query: CallbackQuery) -> None:
    """Show change min price."""
    logger.info('filter_change_min_price')

    filters_config = storage.get_user_settings(query.from_user.id)

    await query.message.edit_text(  # type: ignore
        text=translation.get_message('filters.description.min_price').format(
            presenter.get_price_human_value(filters_config.min_price),
        ),
        reply_markup=presenter.get_filters_min_price_menu(query.from_user.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:min_price:reset')
async def filter_change_min_price_reset(query: CallbackQuery) -> None:
    """Reset min price filter to default value."""
    logger.info(f'filter_change_min_price_reset {query.data=}')
    filters_config = storage.get_user_settings(query.from_user.id)
    if filters_config.min_price is not None:
        storage.update_user_settings(user_id=query.from_user.id, min_price=None)
        return await filter_change_min_price(query)


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:min_price:change')
async def filter_change_min_price_change(query: CallbackQuery, state: FSMContext) -> None:
    """Change min price filter value input."""
    logger.info('filter_change_min_price_change')
    await state.set_state(Form.min_price)

    filters_config = storage.get_user_settings(query.from_user.id)
    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description.min_price.input', filters_config.lang),
        reply_markup=presenter.get_filters_min_price_internal_menu(query.from_user.id),
    )


@dp.message(Form.min_price)
async def filter_change_min_price_change_process(message: Message, state: FSMContext) -> None:
    """Change min price filter value processing."""
    logger.info('filter_change_min_price_change_process')

    try:
        threshold = int(message.text.strip().lower())  # type: ignore
    except (ValueError, AttributeError):
        threshold = 0

    if threshold <= 0:
        await message.reply(translation.get_message('filters.description.min_price.invalid'))
        return

    storage.update_user_settings(user_id=message.chat.id, min_price=threshold)
    await state.clear()

    filters_config = storage.get_user_settings(message.chat.id)

    await message.answer(  # type: ignore
        text=translation.get_message('filters.description.min_price').format(
            presenter.get_price_human_value(filters_config.min_price),
        ),
        reply_markup=presenter.get_filters_min_price_menu(message.chat.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:max_price:show')
async def filter_change_max_price(query: CallbackQuery) -> None:
    """Show change max price."""
    logger.info('filter_change_max_price')

    filters_config = storage.get_user_settings(query.from_user.id)

    await query.message.edit_text(  # type: ignore
        text=translation.get_message('filters.description.max_price').format(
            presenter.get_price_human_value(filters_config.max_price),
        ),
        reply_markup=presenter.get_filters_max_price_menu(query.from_user.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:max_price:reset')
async def filter_change_max_price_reset(query: CallbackQuery) -> None:
    """Reset max price filter to default value."""
    logger.info(f'filter_change_max_price_reset {query.data=}')
    filters_config = storage.get_user_settings(query.from_user.id)
    if filters_config.max_price is not None:
        storage.update_user_settings(user_id=query.from_user.id, max_price=None)
        return await filter_change_max_price(query)


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:max_price:change')
async def filter_change_max_price_change(query: CallbackQuery, state: FSMContext) -> None:
    """Change max price filter value input."""
    logger.info('filter_change_max_price_change')
    await state.set_state(Form.max_price)

    filters_config = storage.get_user_settings(query.from_user.id)
    await query.message.edit_text(  # type: ignore
        text=translation.get_i8n_text('filters.description.max_price.input', filters_config.lang),
        reply_markup=presenter.get_filters_max_price_internal_menu(query.from_user.id),
    )


@dp.message(Form.max_price)
async def filter_change_max_price_change_process(message: Message, state: FSMContext) -> None:
    """Change max price filter value processing."""
    logger.info('filter_change_max_price_change_process')

    try:
        threshold = int(message.text.strip().lower())  # type: ignore
    except (ValueError, AttributeError):
        threshold = 0

    if threshold <= 0:
        await message.reply(translation.get_message('filters.description.max_price.invalid'))
        return

    storage.update_user_settings(user_id=message.chat.id, max_price=threshold)
    await state.clear()

    filters_config = storage.get_user_settings(message.chat.id)

    await message.answer(  # type: ignore
        text=translation.get_message('filters.description.max_price').format(
            presenter.get_price_human_value(filters_config.max_price),
        ),
        reply_markup=presenter.get_filters_max_price_menu(message.chat.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'trial:activate')
async def got_trial(query: CallbackQuery) -> None:
    """Process free trial."""
    if storage.has_used_trial(query.from_user.id, 'trial'):
        logger.error('Trial already used')
        await query.answer(text=translation.get_message('trial.already_used'))
        return

    sub: types.Subscription = storage.renew_subscription(
        user_id=query.from_user.id,
        days=app_settings.TRIAL_PERIOD_DAYS,
    )
    storage.mark_used_trial(query.from_user.id, 'trial')

    await query.message.answer(  # type: ignore
        text=translation.get_message('payment.accepted').format(sub.expired_at.isoformat()),
        reply_markup=presenter.get_main_menu(query.from_user.id),
    )
    await query.message.answer(  # type: ignore
        text=translation.get_message('start.set_filters'),
    )


@dp.callback_query(lambda callback: callback.data and callback.data.startswith('buy:'))
async def buy(query: CallbackQuery) -> None:
    """Send invoice."""
    logger.info('buy')
    settings = storage.get_user_settings(query.from_user.id)

    try:
        price_amount = int(query.data.split(':')[-1])  # type: ignore
        price = prices_settings[price_amount]
    except (AttributeError, IndexError, ValueError, KeyError):
        logger.error(f'Invalid buy request {query}')
        return

    invoice_hash = storage.create_invoice(
        user_id=query.from_user.id,
        price=price.cost,
        days=price.days,
    )
    logger.info('sent invoice {0}, {1}, {2}'.format(
        invoice_hash,
        price,
        query.from_user.id,
    ))
    await query.message.answer_invoice(  # type: ignore
        title=translation.get_i8n_text(price.slug, settings.lang),
        description=translation.get_i8n_text('invoice.description', settings.lang),
        payload=invoice_hash,
        currency='XTR',
        prices=[
            LabeledPrice(
                label=translation.get_i8n_text(price.slug, settings.lang),
                amount=price.cost,
            ),
        ],
    )


@dp.pre_checkout_query()
async def pre_checkout_query(query: PreCheckoutQuery) -> None:
    """Pre checkout check."""
    logger.info(f'Pre checkout request {query=}')

    invoice = storage.get_invoice(query.invoice_payload)
    logger.info(f'{invoice=}')
    if not invoice:
        logger.error('Invoice not found')
        await query.answer(ok=False, error_message=translation.get_message('invoice.expired'))
        return

    if invoice.user_id != query.from_user.id or invoice.price != query.total_amount:
        logger.error('Invoice invalid')
        await query.answer(ok=False, error_message=translation.get_message('invoice.invalid'))
        return

    await query.answer(ok=True)


@dp.message(F.successful_payment)
async def payment_success(message: Message, bot: Bot) -> None:
    """Success purchase."""
    logger.info(f'Payment success {message=}')

    success_payment = message.successful_payment
    if not success_payment:
        raise RuntimeError('Invalid success payment request')

    invoice = storage.get_invoice(success_payment.invoice_payload)  # type: ignore
    logger.info(f'{invoice=}')
    if not invoice:
        logger.error('Invoice not found!')
        await bot.refund_star_payment(
            user_id=message.chat.id,
            telegram_payment_charge_id=success_payment.telegram_payment_charge_id,
        )
        return

    storage.delete_invoice(success_payment.invoice_payload)
    sub: types.Subscription = storage.renew_subscription(
        user_id=message.chat.id,
        days=invoice.days,
    )

    await message.answer(
        text=translation.get_message('payment.accepted').format(sub.expired_at.isoformat()),
        reply_markup=presenter.get_main_menu(message.chat.id),
    )


async def _show_last_estate(filters: types.UserFilters, message: Message) -> None:
    last_ads = await api_client.fetch_estates_all(limit=app_settings.FETCH_ADS_LIMIT)
    logger.info('_show_last_estate: got {0}'.format(len(last_ads)))
    counter = 0
    for ads in last_ads:
        if filters.is_compatible(ads):
            settings = presenter.get_estate_post_settings(ads)
            logger.info(f'publish {settings=}')
            try:
                await message.answer_photo(**settings)
            except Exception as exc:
                logger.error(f'Exception {exc=}')
            counter += 1

        if counter >= app_settings.SHOW_ADS_LIMIT:
            return

    if counter > 0:
        await message.answer(
            text=translation.get_message('estates.example'),
        )


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    asyncio.run(dp.start_polling(bot_instance))
