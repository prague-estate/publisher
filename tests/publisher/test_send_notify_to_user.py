from aiogram import Bot

from publisher.components import storage
from publisher.publisher import _send_notify_to_user
from publisher.settings import app_settings


async def test_send_notify_to_user_smoke(fixture_estate_item):
    storage.update_user_settings(1, enabled=True)
    assert storage.get_user_settings(1).is_enabled_notifications is True

    async with Bot(app_settings.BOT_TOKEN) as bot_instance:
        res = await _send_notify_to_user(bot_instance, user_id=1, ads_for_post=fixture_estate_item)

    assert res is None
    assert storage.get_user_settings(1).is_enabled_notifications is False
