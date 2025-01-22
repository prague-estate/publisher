from unittest.mock import AsyncMock

import pytest

from publisher import bot
from publisher.storage import update_user_filter, get_user_filters


@pytest.mark.parametrize('filters_enabled, expected_state', [
    (True, False),
    (False, True),
])
async def test_filter_change_enabled_happy_path(filters_enabled: bool, expected_state: bool):
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    update_user_filter(query_mock.from_user.id, enabled=filters_enabled)

    await bot.filter_change_enabled(query_mock)

    query_mock.message.edit_reply_markup.assert_called_once()
    assert get_user_filters(query_mock.from_user.id).enabled is expected_state
