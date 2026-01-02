from unittest.mock import AsyncMock

import pytest

from publisher import bot
from publisher.components.storage import get_user_settings, update_user_settings


@pytest.mark.parametrize('payload, current_state, expected_state', [
    ('filters:layout:reset', None, None),
    ('filters:layout:reset', {'three_kk', 'four_kk'}, None),

    ('filters:layout:switch:two_one', None, {'two_one'}),
    ('filters:layout:switch:two_one', {'two_one'}, None),
    ('filters:layout:switch:two_one', {'three_kk', 'four_kk'}, {'three_kk', 'four_kk', 'two_one'}),
    ('filters:layout:switch:two_one', {'two_one', 'four_kk'}, {'four_kk'}),

    ('filters:layout:switch:invalid', {'two_one', 'four_kk'}, {'two_one', 'four_kk'}),

])
async def test_filter_change_layout_switch_happy_path(payload, current_state, expected_state):
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    query_mock.data = payload
    update_user_settings(user_id=query_mock.from_user.id, layouts=current_state)

    await bot.filter_change_layout_switch(query_mock)

    assert get_user_settings(user_id=query_mock.from_user.id).layouts == expected_state
