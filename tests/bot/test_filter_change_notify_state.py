from unittest.mock import AsyncMock

import pytest

from publisher import bot
from publisher.storage import get_user_filters, update_user_filter


@pytest.mark.parametrize('filters_enabled, expected_state', [
    (True, False),
    (False, True),
])
async def test_filter_change_notify_state(filters_enabled: bool, expected_state: bool):
    message_mock = AsyncMock()
    message_mock.chat.id = 1
    update_user_filter(message_mock.chat.id, enabled=filters_enabled)

    await bot.filter_change_notify_state(message_mock)

    message_mock.answer.assert_called_once()
    assert get_user_filters(message_mock.chat.id).enabled is expected_state
