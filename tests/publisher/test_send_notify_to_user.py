from aiogram import Bot

from publisher import storage
from publisher.publisher import _send_notify_to_user
from publisher.settings import app_settings


async def test_send_notify_to_user_smoke():
    storage.update_user_filter(1, enabled=True)
    assert storage.get_user_filters(1).is_enabled is True

    async with Bot(app_settings.BOT_TOKEN) as bot_instance:
        res = await _send_notify_to_user(bot_instance, user_id=1, caption='test', photo='test_url')

    assert res is None
    assert storage.get_user_filters(1).is_enabled is False
