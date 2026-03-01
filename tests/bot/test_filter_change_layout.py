from unittest.mock import AsyncMock

import publisher.handlers.filter_layout


async def test_filter_change_layout_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1

    await publisher.handlers.filter_layout.filter_change_layout(query_mock)

    query_mock.message.edit_text.assert_called_once()
