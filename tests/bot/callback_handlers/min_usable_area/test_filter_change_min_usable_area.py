from unittest.mock import AsyncMock

from publisher.components import callback_handlers


async def test_filter_change_min_usable_area_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1

    await callback_handlers.filter_change_min_usable_area(query_mock)

    query_mock.message.edit_text.assert_called_once()
