from unittest.mock import AsyncMock

from publisher import bot


async def test_buy_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    query_mock.data = 'filters:back'

    await bot.filter_go_back(query_mock)

    query_mock.message.edit_text.assert_called_once()