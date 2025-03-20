
from unittest.mock import AsyncMock

import pytest

from publisher import bot
from publisher.storage import get_user_filters


@pytest.mark.parametrize('payload, success', [
    ('', False),
    ('123,', False),
    ('sss', False),
    (' 1234   ', True),
])
async def test_filter_change_min_price_change_happy_path(payload: str, success: bool):
    message_mock = AsyncMock()
    message_mock.chat.id = 1
    message_mock.text = payload
    state_mock = AsyncMock()

    await bot.filter_change_min_price_change_process(message_mock, state_mock)

    if success:
        state_mock.clear.assert_called_once()
        message_mock.answer.assert_called_once()
        assert get_user_filters(user_id=1).min_price == int(payload)

    else:
        message_mock.reply.assert_called_once()

