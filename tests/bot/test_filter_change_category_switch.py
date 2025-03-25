from unittest.mock import AsyncMock

import pytest

from publisher import bot
from publisher.storage import get_user_filters, update_user_filter


@pytest.mark.parametrize('payload, current_state, expected_state', [
    ('filters:category:reset', None, None),
    ('filters:category:reset', 'sale', None),

    ('filters:category:sale', None, 'sale'),
    ('filters:category:sale', 'sale', 'sale'),
    ('filters:category:sale', 'lease', 'sale'),

    ('filters:category:lease', None, 'lease'),
    ('filters:category:lease', 'lease', 'lease'),
    ('filters:category:lease', 'sale', 'lease'),
])
async def test_filter_change_category_switch_happy_path(payload, current_state, expected_state):
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    query_mock.data = payload
    update_user_filter(user_id=query_mock.from_user.id, category=current_state)

    await bot.filter_change_category_switch(query_mock)

    assert get_user_filters(user_id=query_mock.from_user.id).category == expected_state
    assert get_user_filters(user_id=query_mock.from_user.id).min_price is None
    assert get_user_filters(user_id=query_mock.from_user.id).max_price is None
