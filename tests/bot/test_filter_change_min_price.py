from unittest.mock import AsyncMock

import publisher.handlers.filter_price


async def test_filter_change_min_price_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1

    await publisher.handlers.filter_price.filter_change_min_price(query_mock)

    query_mock.message.edit_text.assert_called_once()
