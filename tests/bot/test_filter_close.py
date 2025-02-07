from unittest.mock import AsyncMock

from publisher import bot


async def test_filter_close_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    query_mock.data = 'filters:back'

    await bot.filter_close(query_mock)

    query_mock.message.delete.assert_called_once()
    query_mock.message.answer.assert_called_once()