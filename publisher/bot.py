"""Telegram bot handlers."""
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from publisher import storage
from publisher.presenter import get_filters_menu, get_main_menu, get_message, get_prices_menu
from publisher.settings import app_settings, prices_settings
from publisher.types import Subscription

logger = logging.getLogger(__file__)

bot_instance = Bot(app_settings.BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: Message) -> None:
    """Welcome message and optional grant promo."""
    logger.info('Welcome')
    await message.answer(
        text=get_message('welcome'),
        reply_markup=get_main_menu(message.chat.id),
    )


@dp.message(Command('support'))
@dp.message(F.text == get_message('support.button'))
async def support(message: Message) -> None:
    """Support link."""
    logger.info('About')
    await message.answer(
        text=get_message('support'),
        reply_markup=get_main_menu(message.chat.id),
    )


@dp.message(F.text.in_({get_message('subscription.button.active'), get_message('subscription.button.inactive')}))
async def user_subscription(message: Message) -> None:
    """Subscription info."""
    logger.info('Subscription')

    sub = storage.get_subscription(message.chat.id)
    if sub and sub.is_active:
        text = get_message('subscription.active').format(sub.expired_at.isoformat())
    else:
        text = get_message('subscription.inactive')

    await message.answer(
        text=text,
        reply_markup=get_prices_menu(),
    )


@dp.message(F.text == get_message('filters.button'))
async def user_filters(message: Message) -> None:
    """User filters setup."""
    logger.info('User filters')

    await message.answer(
        text=get_message('filters.description'),
        reply_markup=get_filters_menu(message.chat.id),
    )


@dp.callback_query(lambda callback: callback.data and callback.data == 'filters:enabled')
async def filter_change_enable(query: CallbackQuery) -> None:
    """Change enabled status."""
    logger.info('filter_change_notifications')
    filters_config = storage.get_user_filters(query.from_user.id)
    if filters_config.enabled:
        storage.update_user_filter(query.from_user.id, enabled=False)
    else:
        storage.update_user_filter(query.from_user.id, enabled=True)

    await query.message.edit_reply_markup(  # type: ignore
        reply_markup=get_filters_menu(query.from_user.id),
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
        description=get_message('invoice.description'),
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
async def pre_checkout_query_handler(query: PreCheckoutQuery) -> None:
    """Pre checkout check."""
    logger.info(f'Pre checkout request {query=}')

    invoice = storage.get_invoice(query.invoice_payload)
    logger.info(f'{invoice=}')
    if not invoice:
        logger.error('Invoice not found')
        await query.answer(ok=False, error_message=get_message('invoice.expired'))
        return

    if invoice.user_id != query.from_user.id or invoice.price != query.total_amount:
        logger.error('Invoice invalid')
        await query.answer(ok=False, error_message=get_message('invoice.invalid'))
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
        text=get_message('payment.accepted').format(sub.expired_at.isoformat()),
        reply_markup=get_main_menu(message.chat.id),
    )


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    asyncio.run(dp.start_polling(bot_instance))
