from unittest.mock import AsyncMock

from publisher import bot


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
