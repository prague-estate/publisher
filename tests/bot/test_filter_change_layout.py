from unittest.mock import AsyncMock

from publisher import bot


async def test_filter_change_layout_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1

    await bot.filter_change_layout(query_mock)

    query_mock.message.edit_text.assert_called_once()
