from unittest import mock

import pytest

from publisher.components.api_client import fetch_estates_all
from publisher.components.types import Estate


async def test_fetch_estates_all_contract():
    response = await fetch_estates_all(limit=2)

    assert isinstance(response[0], Estate)


@pytest.mark.parametrize('limit', [0, 1, 2])
async def test_fetch_estates_all_limit(limit: int):
    response = await fetch_estates_all(limit=limit)

    assert len(response) == limit


async def test_fetch_estates_all_failed():
    with mock.patch('publisher.components.api_client.aiohttp.ClientSession.get') as mock_get:
        mock_get.side_effect = KeyError()
        response = await fetch_estates_all(limit=1)
        assert response == []
