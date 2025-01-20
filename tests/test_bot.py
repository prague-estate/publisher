from unittest.mock import AsyncMock, Mock

import pytest

from publisher import bot
from publisher.storage import create_invoice, get_invoice, renew_subscription, update_user_filter, get_user_filters


@pytest.mark.parametrize('handler_name', [
    'start',
    'support',
    'user_subscription',
    'user_filters',
])
@pytest.mark.parametrize('subscription_active', [True, False])
@pytest.mark.parametrize('filters_enabled', [True, False])
async def test_handler_answer_smoke(
    fixture_empty_storage,
    handler_name: str,
    subscription_active: bool,
    filters_enabled: bool,
):
    message_mock = AsyncMock()
    message_mock.chat.id = 1
    if subscription_active:
        renew_subscription(user_id=1, days=1)
    if filters_enabled:
        update_user_filter(user_id=1, enabled=True)

    await getattr(bot, handler_name)(message=message_mock)

    message_mock.answer.assert_called_once()


async def test_payment_success_happy_path():
    payment = Mock()
    payment.invoice_payload = create_invoice(user_id=1, price=2, days=3)
    payment.telegram_payment_charge_id = '111'
    message_mock = AsyncMock()
    message_mock.successful_payment = payment
    message_mock.chat.id = 1

    await bot.payment_success(message_mock, AsyncMock())

    message_mock.answer.assert_called_once()
    assert get_invoice(payment.invoice_payload) is None


async def test_payment_success_invoice_not_found():
    payment = Mock()
    payment.invoice_payload = 'invalid-hash'
    payment.telegram_payment_charge_id = '111'
    message_mock = AsyncMock()
    message_mock.successful_payment = payment
    message_mock.chat.id = 1
    bot_mock = AsyncMock()

    await bot.payment_success(message_mock, bot_mock)

    bot_mock.refund_star_payment.assert_called_once()


@pytest.mark.parametrize('filters_enabled, expected_state', [
    (True, False),
    (False, True),
])
async def test_filter_change_enable_happy_path(filters_enabled: bool, expected_state: bool):
    query_mock = AsyncMock()
    query_mock.from_user.id = 1

    await bot.filter_change_enable(query_mock)

    query_mock.message.edit_reply_markup.assert_called_once()
    assert get_user_filters(query_mock.from_user.id).enabled is expected_state


async def test_buy_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    query_mock.data = 'buy:50'

    await bot.buy(query_mock)

    query_mock.message.answer_invoice.assert_called_once()


async def test_buy_invalid_price():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    query_mock.data = 'buy:7'

    await bot.buy(query_mock)

    query_mock.message.answer_invoice.assert_not_called()


async def test_pre_checkout_query_handler_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    query_mock.invoice_payload = create_invoice(user_id=1, price=2, days=3)
    query_mock.total_amount = 2

    await bot.pre_checkout_query_handler(query_mock)

    query_mock.answer.assert_called_once()
