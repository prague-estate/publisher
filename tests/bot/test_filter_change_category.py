from unittest.mock import AsyncMock

import publisher.handlers.filter_category


async def test_filter_change_category_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1

    await publisher.handlers.filter_category.filter_change_category(query_mock)

    query_mock.message.edit_text.assert_called_once()
