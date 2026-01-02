from unittest.mock import AsyncMock

import pytest

from publisher import bot
from publisher.components.storage import get_user_filters, update_user_filter


@pytest.mark.parametrize('payload, current_state, expected_state', [
    ('filters:district:reset', None, None),
    ('filters:district:reset', {7, 6}, None),

    ('filters:district:switch:7', None, {7}),
    ('filters:district:switch:7', {7}, None),
    ('filters:district:switch:7', {7, 8, 22}, {8, 22}),
    ('filters:district:switch:7', {8, 22}, {7, 8, 22}),

    ('filters:district:switch:0', {7, 8, 22}, {7, 8, 22}),
    ('filters:district:switch:invalid', {7, 8, 22}, {7, 8, 22}),
])
async def test_filter_change_district_switch_happy_path(payload, current_state, expected_state):
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    query_mock.data = payload
    update_user_filter(user_id=query_mock.from_user.id, districts=current_state)

    await bot.filter_change_district_switch(query_mock)

    assert get_user_filters(user_id=query_mock.from_user.id).districts == expected_state
