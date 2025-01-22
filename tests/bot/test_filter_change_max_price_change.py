from unittest.mock import AsyncMock

from publisher import bot


async def test_filter_change_max_price_change_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    state_mock = AsyncMock()

    await bot.filter_change_max_price_change(query_mock, state_mock)

    state_mock.set_state.assert_called_once()
    query_mock.message.edit_text.assert_called_once()
