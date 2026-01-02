from unittest.mock import AsyncMock

import pytest

from publisher import bot
from publisher.components.storage import get_user_settings, update_user_settings


@pytest.mark.parametrize('filters_enabled, expected_state', [
    (True, False),
    (False, True),
])
async def test_user_settings_toggle_notifications(filters_enabled: bool, expected_state: bool):
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    update_user_settings(query_mock.from_user.id, enabled=filters_enabled)

    await bot.user_settings_toggle_notifications(query_mock)

    assert get_user_settings(query_mock.from_user.id).enabled is expected_state
