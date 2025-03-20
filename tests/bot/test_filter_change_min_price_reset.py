from unittest.mock import AsyncMock

import pytest

from publisher import bot
from publisher.storage import get_user_filters, update_user_filter


@pytest.mark.parametrize('payload, expected_state', [
    (None, None),
    (0, None),
    (100500, None),
])
async def test_filter_change_min_price_reset_happy_path(payload, expected_state):
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    update_user_filter(query_mock.from_user.id, min_price=payload)

    await bot.filter_change_min_price_reset(query_mock)

    assert get_user_filters(query_mock.from_user.id).min_price is expected_state
