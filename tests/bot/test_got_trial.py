from unittest.mock import AsyncMock

from publisher import bot
from publisher.components.storage import get_subscription, mark_used_trial


async def test_got_trial_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1

    await bot.got_trial(query_mock)

    assert query_mock.message.answer.call_count >= 1
    assert get_subscription(user_id=1).is_active


async def test_got_trial_already_used():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    mark_used_trial(1, 'trial')

    await bot.got_trial(query_mock)

    query_mock.answer.assert_called_once()
    assert get_subscription(user_id=1) is None
