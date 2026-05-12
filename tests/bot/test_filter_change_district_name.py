from unittest.mock import AsyncMock

from publisher.handlers.filter_district_name import filter_change_district_name


async def test_filter_change_district_name_happy_path():
    query_mock = AsyncMock()
    query_mock.from_user.id = 1
    query_mock.data = 'filters:district_name:show:1'

    await filter_change_district_name(query_mock)

    query_mock.message.edit_text.assert_called_once()
