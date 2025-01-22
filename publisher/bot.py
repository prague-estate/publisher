"""Telegram bot handlers."""
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from publisher import presenter, storage, translation
from publisher.settings import app_settings, prices_settings
from publisher.types import Subscription

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
@dp.message(F.text == translation.get_message('support.button'))
async def about(message: Message) -> None:
    """About project."""
    logger.info('About')
    await message.answer(
        text=translation.get_message('support'),
        reply_markup=presenter.get_main_menu(message.chat.id),
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
