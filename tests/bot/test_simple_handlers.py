from unittest.mock import AsyncMock

import pytest

from publisher import bot
from publisher.components.storage import renew_subscription, update_user_filter


@pytest.mark.parametrize('handler_name', [
    'about',
    'user_subscription',
    'user_filters',
])
@pytest.mark.parametrize('subscription_active', [True, False])
@pytest.mark.parametrize('filters_enabled', [True, False])
async def test_handler_answer_smoke(
    handler_name: str,
    subscription_active: bool,
    filters_enabled: bool,
):
    message_mock = AsyncMock()
    message_mock.chat.id = 1
    if subscription_active:
        renew_subscription(user_id=1, days=1)
    if filters_enabled:
        update_user_filter(user_id=1, enabled=True)

    await getattr(bot, handler_name)(message=message_mock)

    message_mock.answer.assert_called_once()
