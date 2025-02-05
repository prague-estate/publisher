from unittest.mock import AsyncMock

from publisher import bot
from publisher.settings import app_settings


async def test_admin_info_auth():
    message_mock = AsyncMock()
    message_mock.chat.id = 1

    await bot.admin_info(message_mock)

    assert message_mock.answer.call_count == 0


async def test_admin_info_happy_path():
    app_settings.ADMINS = '1;2'

    message_mock = AsyncMock()
    message_mock.chat.id = 1

    await bot.admin_info(message_mock)

    message_mock.answer.assert_called_once()
