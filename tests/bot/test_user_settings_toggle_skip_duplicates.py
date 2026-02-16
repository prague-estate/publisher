from unittest.mock import AsyncMock

import pytest

from publisher import bot
from publisher.components.storage import get_user_settings, update_user_settings


@pytest.mark.parametrize('filters_skip_duplicates, expected_state', [
    (True, False),
    (False, True),
])
async def test_user_settings_toggle_skip_duplicates(filters_skip_duplicates: bool, expected_state: bool):
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    update_user_settings(query_mock.from_user.id, skip_duplicates=filters_skip_duplicates)

    await bot.user_settings_toggle_skip_duplicates(query_mock)

    assert get_user_settings(query_mock.from_user.id).skip_duplicates is expected_state
