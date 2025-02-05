"""Telegram bot handlers."""
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery
from aiogram.utils.deep_linking import create_start_link

from publisher import api, presenter, storage, translation
from publisher.settings import app_settings, prices_settings
from publisher.types import Estate, Subscription

logger = logging.getLogger(__file__)

bot_instance = Bot(app_settings.BOT_TOKEN)
dp = Dispatcher(storage=RedisStorage.from_url(app_settings.REDIS_DSN))


class Form(StatesGroup):
    """Change filters states."""

    max_price = State()


@dp.message(CommandStart(deep_link=True))
async def start(message: Message, command: CommandObject) -> None:
    """Apply promo trial if exists."""
    promo = str(command.args).strip().lower()
    logger.info(f'Start {promo=}')
    await about(message)

    promo_days: int | None = app_settings.PROMO_CODES.get(promo)

    if promo_days and not storage.has_used_trial(message.chat.id, promo):
        logger.info('apply promo code')
        sub: Subscription = storage.renew_subscription(
            user_id=message.chat.id,
            days=promo_days,
        )
        storage.mark_used_trial(message.chat.id, promo)

        await message.answer(  # type: ignore
            text=translation.get_message('payment.accepted').format(sub.expired_at.isoformat()),
            reply_markup=presenter.get_main_menu(message.chat.id),
        )


@dp.message(Command('start'))
@dp.message(Command('support'))
@dp.message(Command('paysupport'))
@dp.message(F.text == translation.get_message('support.button'))
async def about(message: Message) -> None:
    """About project."""
    logger.info('About')
    await message.answer(
        text=translation.get_message('support'),
        reply_markup=presenter.get_main_menu(message.chat.id),
    )


@dp.message(F.text == translation.get_message('estates.button'))
async def show_estates(message: Message) -> None:  # noqa: WPS217
    """Show estates by user filters."""
    logger.info('Estates')

    subscription = storage.get_subscription(message.chat.id)
    if not subscription or not subscription.is_active:
        await user_subscription(message)
        return

    filters_config = storage.get_user_filters(message.chat.id)
    last_ads = await api.fetch_estates_all(limit=app_settings.FETCH_ADS_LIMIT)

    selected_ads: list[Estate] = []
    for ads in last_ads:
        if filters_config.is_compatible(ads):
            selected_ads.append(ads)
        if len(selected_ads) >= app_settings.SHOW_ADS_LIMIT:
            break

    if not selected_ads:
        await message.answer(
            text=translation.get_message('estates.not_found'),
            reply_markup=presenter.get_main_menu(message.chat.id),
        )
        return

    for ads_for_post in selected_ads[::-1]:
        settings = presenter.get_estate_post_settings(ads_for_post)
        await message.answer_photo(**settings)

    if filters_config.enabled:
        await message.answer(
            text=translation.get_message('estates.wait_fot_new'),
            reply_markup=presenter.get_main_menu(message.chat.id),
        )

    else:
        await message.answer(
            text=translation.get_message('estates.enable_filters_request'),
        )
        await user_filters(message)


@dp.message(F.text == translation.get_message('admin.button'))
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

    await message.answer(
        text='\n'.join(response_messages),
        reply_markup=presenter.get_main_menu(message.chat.id),
        parse_mode='Markdown',
    )


@dp.message(F.text.in_({
    translation.get_message('subscription.button.active'),
    translation.get_message('subscription.button.inactive'),
}))
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


@dp.message(F.text == translation.get_message('filters.button'))
async def user_filters(message: Message) -> None:
    """User filters setup."""
    logger.info('User filters')

    await message.answer(
        text=translation.get_message('filters.description'),
        reply_markup=presenter.get_filters_menu(message.chat.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:back')
async def filter_go_back(query: CallbackQuery, state: FSMContext | None = None) -> None:
    """Show filters."""
    logger.info('filter_go_back')

    if state:
        await state.clear()

    await query.message.edit_text(  # type: ignore
        text=translation.get_message('filters.description'),
        reply_markup=presenter.get_filters_menu(query.from_user.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:enabled:change')
async def filter_change_enabled(query: CallbackQuery) -> None:
    """Change enabled status."""
    logger.info('filter_change_notifications')
    filters_config = storage.get_user_filters(query.from_user.id)
    if filters_config.enabled:
        storage.update_user_filter(query.from_user.id, enabled=False)
    else:
        storage.update_user_filter(query.from_user.id, enabled=True)

    await query.message.edit_reply_markup(  # type: ignore
        reply_markup=presenter.get_filters_menu(query.from_user.id),
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
    filters_config = storage.get_user_filters(query.from_user.id)
    logger.info(f'filter_change_district_switch {query.data=} {filters_config.districts=}')
    district_for_switch = query.data.split(':')[-1]  # type: ignore

    if district_for_switch == 'reset':
        logger.info('filter_change_district_switch: reset')
        if filters_config.districts is not None:
            storage.update_user_filter(user_id=query.from_user.id, districts=None)
            await filter_change_district(query)
        return None

    if not district_for_switch.isdigit() or int(district_for_switch) not in app_settings.ENABLED_DISTRICTS:
        logger.error('invalid district value got!')
        return None

    district_for_switch = int(district_for_switch)
    if filters_config.districts is None:
        logger.info('filter_change_district_switch: enable from not set')
        storage.update_user_filter(
            user_id=query.from_user.id,
            districts={district_for_switch},
        )
        return await filter_change_district(query)

    elif district_for_switch in filters_config.districts:
        new_value = (filters_config.districts - {district_for_switch}) or None
        logger.info(f'filter_change_district_switch: disable, {new_value=}')
        storage.update_user_filter(
            user_id=query.from_user.id,
            districts=new_value,
        )
        return await filter_change_district(query)

    new_value = filters_config.districts | {district_for_switch}
    logger.info(f'filter_change_district_switch: enable, {new_value=}')
    storage.update_user_filter(
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
    filters_config = storage.get_user_filters(query.from_user.id)
    logger.info(f'filter_change_layout_switch {query.data=} {filters_config.layouts=}')
    layout_for_switch: str = query.data.split(':')[-1]  # type: ignore

    if layout_for_switch == 'reset':
        logger.info('filter_change_layout_switch: reset')
        if filters_config.layouts is not None:
            storage.update_user_filter(user_id=query.from_user.id, layouts=None)
            await filter_change_layout(query)
        return None

    if layout_for_switch not in app_settings.ENABLED_LAYOUTS:
        logger.error('invalid layout value got!')
        return None

    if filters_config.layouts is None:
        logger.info('filter_change_layout_switch: enable from not set')
        storage.update_user_filter(
            user_id=query.from_user.id,
            layouts={layout_for_switch},
        )
        return await filter_change_layout(query)

    elif layout_for_switch in filters_config.layouts:
        new_value = (filters_config.layouts - {layout_for_switch}) or None
        logger.info(f'filter_change_layout_switch: disable, {new_value=}')
        storage.update_user_filter(
            user_id=query.from_user.id,
            layouts=new_value,
        )
        return await filter_change_layout(query)

    new_value = filters_config.layouts | {layout_for_switch}
    logger.info(f'filter_change_layout_switch: enable, {new_value=}')
    storage.update_user_filter(
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
    filters_config = storage.get_user_filters(query.from_user.id)

    if category_for_enable == 'reset':
        logger.info('filter_change_category_switch: reset')
        if filters_config.category is not None:
            storage.update_user_filter(user_id=query.from_user.id, category=None)
            return await filter_change_category(query)

    elif filters_config.category != category_for_enable:
        logger.info(f'filter_change_category_switch: enable {category_for_enable}')
        storage.update_user_filter(user_id=query.from_user.id, category=category_for_enable)
        return await filter_change_category(query)


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:max_price:show')
async def filter_change_max_price(query: CallbackQuery) -> None:
    """Show change max price."""
    logger.info('filter_change_max_price')

    filters_config = storage.get_user_filters(query.from_user.id)

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
    filters_config = storage.get_user_filters(query.from_user.id)
    if filters_config.max_price is not None:
        storage.update_user_filter(user_id=query.from_user.id, max_price=None)
        return await filter_change_max_price(query)


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:max_price:change')
async def filter_change_max_price_change(query: CallbackQuery, state: FSMContext) -> None:
    """Change max price filter value input."""
    logger.info('filter_change_max_price_change')
    await state.set_state(Form.max_price)

    await query.message.edit_text(  # type: ignore
        text=translation.get_message('filters.description.max_price.input'),
        reply_markup=presenter.get_filters_max_price_internal_menu(),
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

    storage.update_user_filter(user_id=message.chat.id, max_price=threshold)
    await state.clear()

    filters_config = storage.get_user_filters(message.chat.id)

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

    sub: Subscription = storage.renew_subscription(
        user_id=query.from_user.id,
        days=app_settings.TRIAL_PERIOD_DAYS,
    )
    storage.mark_used_trial(query.from_user.id, 'trial')

    await query.message.answer(  # type: ignore
        text=translation.get_message('payment.accepted').format(sub.expired_at.isoformat()),
        reply_markup=presenter.get_main_menu(query.from_user.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data.startswith('buy:'))
async def buy(query: CallbackQuery) -> None:
    """Send invoice."""
    logger.info('buy')
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
        title=price.title,
        description=translation.get_message('invoice.description'),
        payload=invoice_hash,
        currency='XTR',
        prices=[
            LabeledPrice(
                label=price.title,
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
    sub: Subscription = storage.renew_subscription(
        user_id=message.chat.id,
        days=invoice.days,
    )

    await message.answer(
        text=translation.get_message('payment.accepted').format(sub.expired_at.isoformat()),
        reply_markup=presenter.get_main_menu(message.chat.id),
    )


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    asyncio.run(dp.start_polling(bot_instance))
