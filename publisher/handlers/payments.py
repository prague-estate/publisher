"""Payment bot handlers."""

import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery

from publisher.components import presenter, storage, translation, types
from publisher.settings import app_settings, prices_settings

logger = logging.getLogger(__file__)
router = Router()


@router.callback_query(lambda callback: callback.data and callback.data == 'trial:activate')
async def got_trial(query: CallbackQuery) -> None:
    """Process free trial."""
    settings = storage.get_user_settings(query.from_user.id)

    if storage.has_used_trial(query.from_user.id, 'trial'):
        logger.error('Trial already used')
        await query.answer(text=translation.get_i8n_text('trial.already_used', settings.lang))
        return

    sub: types.Subscription = storage.renew_subscription(
        user_id=query.from_user.id,
        days=app_settings.TRIAL_PERIOD_DAYS,
    )
    storage.mark_used_trial(query.from_user.id, 'trial')

    await query.message.answer(  # type: ignore
        text=translation.get_i8n_text('payment.accepted', settings.lang).format(sub.expired_at.isoformat()),
        reply_markup=presenter.get_main_menu(query.from_user.id),
    )
    await query.message.answer(  # type: ignore
        text=translation.get_i8n_text('start.set_filters', settings.lang),
    )


@router.callback_query(lambda callback: callback.data and callback.data.startswith('buy:'))
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


@router.pre_checkout_query()
async def pre_checkout_query(query: PreCheckoutQuery) -> None:
    """Pre checkout check."""
    logger.info(f'Pre checkout request {query=}')
    settings = storage.get_user_settings(query.from_user.id)

    invoice = storage.get_invoice(query.invoice_payload)
    logger.info(f'{invoice=}')
    if not invoice:
        logger.error('Invoice not found')
        await query.answer(ok=False, error_message=translation.get_i8n_text('invoice.expired', settings.lang))
        return

    if invoice.user_id != query.from_user.id or invoice.price != query.total_amount:
        logger.error('Invoice invalid')
        await query.answer(ok=False, error_message=translation.get_i8n_text('invoice.invalid', settings.lang))
        return

    await query.answer(ok=True)


@router.message(F.successful_payment)
async def payment_success(message: Message, bot: Bot) -> None:
    """Success purchase."""
    logger.info(f'Payment success {message=}')
    settings = storage.get_user_settings(message.chat.id)

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
        text=translation.get_i8n_text('payment.accepted', settings.lang).format(sub.expired_at.isoformat()),
        reply_markup=presenter.get_main_menu(message.chat.id),
    )



def init(dp: Dispatcher) -> None:
    """Routers setup."""
    dp.include_router(router)
