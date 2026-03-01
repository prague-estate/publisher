from unittest.mock import AsyncMock

import publisher.handlers.user_settings


async def test_user_settings_close_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    query_mock.data = 'settings:back'

    await publisher.handlers.user_settings.user_settings_close(query_mock)

    query_mock.message.delete.assert_called_once()
    query_mock.message.answer.assert_called_once()