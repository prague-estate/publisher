from unittest.mock import AsyncMock, Mock

from publisher.components.storage import create_invoice, get_invoice
from publisher.handlers import payments


async def test_payment_success_happy_path():
    payment = Mock()
    payment.invoice_payload = create_invoice(user_id=1, price=2, days=3)
    payment.telegram_payment_charge_id = '111'
    message_mock = AsyncMock()
    message_mock.successful_payment = payment
    message_mock.chat.id = 1

    await payments.payment_success(message_mock, AsyncMock())

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

    await payments.payment_success(message_mock, bot_mock)

    bot_mock.refund_star_payment.assert_called_once()
