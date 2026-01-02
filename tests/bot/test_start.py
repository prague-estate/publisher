from unittest.mock import AsyncMock

import pytest

from publisher import bot
from publisher.components.storage import get_subscription


@pytest.mark.parametrize('promo, expected', [
    (None, False),
    ('invalid', False),
    ('vas3k', True),
])
async def test_start_with_promo(
    promo: str | None,
    expected: bool,
):
    message_mock = AsyncMock()
    message_mock.chat.id = 1
    command_mock = AsyncMock()
    command_mock.args = promo

    await bot.start(message=message_mock, command=command_mock)

    if expected:
        assert message_mock.answer.call_count == 2
        assert get_subscription(user_id=1).is_active
    else:
        assert message_mock.answer.call_count == 1
        assert get_subscription(user_id=1) is None
