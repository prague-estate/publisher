from unittest.mock import AsyncMock

import pytest

from publisher.handlers import filter_usable_area
from publisher.components.storage import get_user_settings, update_user_settings


@pytest.mark.parametrize('payload, expected_state', [
    (None, None),
    (0, None),
    (100500, None),
])
async def test_filter_change_min_usable_area_reset_happy_path(payload, expected_state):
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    update_user_settings(query_mock.from_user.id, min_usable_area=payload)

    await filter_usable_area.filter_change_min_usable_area_reset(query_mock)

    assert get_user_settings(query_mock.from_user.id).min_usable_area is expected_state
