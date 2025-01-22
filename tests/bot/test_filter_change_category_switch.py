from unittest.mock import AsyncMock

import pytest

from publisher import bot
from publisher.storage import update_user_filter, get_user_filters


@pytest.mark.parametrize('payload, current_state, expected_state', [
    ('filters:category:reset', None, None),
    ('filters:category:reset', 'sale', None),

    ('filters:category:enable:sale', None, 'sale'),
    ('filters:category:enable:sale', 'sale', 'sale'),
    ('filters:category:enable:sale', 'rent', 'sale'),

    ('filters:category:enable:rent', None, 'rent'),
    ('filters:category:enable:rent', 'rent', 'rent'),
    ('filters:category:enable:rent', 'sale', 'rent'),
])
async def test_filter_change_category_switch_happy_path(payload, current_state, expected_state):
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    query_mock.data = payload
    update_user_filter(user_id=query_mock.from_user.id, category=current_state)

    await bot.filter_change_category_switch(query_mock)

    assert get_user_filters(user_id=query_mock.from_user.id).category == expected_state
