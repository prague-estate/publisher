from unittest.mock import AsyncMock

from publisher import bot
from publisher.storage import create_invoice


async def test_pre_checkout_query_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    query_mock.invoice_payload = create_invoice(user_id=1, price=2, days=3)
    query_mock.total_amount = 2

    await bot.pre_checkout_query(query_mock)

    query_mock.answer.assert_called_once()
