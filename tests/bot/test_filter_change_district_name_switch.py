from unittest.mock import AsyncMock

import pytest

from publisher.components.storage import get_user_settings, update_user_settings
from publisher.handlers.filter_district_name import filter_change_district_name_switch


@pytest.mark.parametrize('payload, current_state, expected_state', [
    ('filters:district_name:reset', None, None),
    ('filters:district_name:reset', {'Smíchov', 'Vinohrady'}, None),

    ('filters:district_name:switch:1:Smíchov', None, {'Smíchov'}),
    ('filters:district_name:switch:1:Smíchov', {'Smíchov'}, None),
    ('filters:district_name:switch:1:Smíchov', {'Smíchov', 'Vinohrady', 'Žižkov'}, {'Vinohrady', 'Žižkov'}),
    ('filters:district_name:switch:1:Smíchov', {'Vinohrady', 'Žižkov'}, {'Smíchov', 'Vinohrady', 'Žižkov'}),

    ('filters:district_name:switch:1:NotARealDistrict', {'Smíchov'}, {'Smíchov'}),
])
async def test_filter_change_district_name_switch_happy_path(payload, current_state, expected_state):
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    query_mock.data = payload
    update_user_settings(user_id=query_mock.from_user.id, district_names=current_state)

    await filter_change_district_name_switch(query_mock)

    assert get_user_settings(user_id=query_mock.from_user.id).district_names == expected_state
