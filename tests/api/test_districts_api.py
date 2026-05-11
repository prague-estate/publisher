from unittest import mock

from publisher.components.api_client import fetch_districts
from publisher.components.types import District


async def test_fetch_districts_contract():
    response = await fetch_districts()

    assert response
    assert isinstance(response[0], District)
    assert isinstance(response[0].name, str)
    assert isinstance(response[0].number, int)
    assert 1 <= response[0].number <= 10


async def test_fetch_districts_failed():
    with mock.patch('publisher.components.api_client.aiohttp.ClientSession.get') as mock_get:
        mock_get.side_effect = KeyError()
        response = await fetch_districts()
        assert response == []
