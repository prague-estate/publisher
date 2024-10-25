import pytest

from publisher.api import fetch_estates
from publisher.types import Estate


async def test_fetch_estates_contract():
    response = await fetch_estates(category='sale', limit=2)

    assert isinstance(response[0], Estate)


@pytest.mark.parametrize('limit', [0, 1, 2])
async def test_fetch_estates_limit(limit: int):
    response = await fetch_estates(category='sale', limit=limit)

    assert len(response) == limit


@pytest.mark.parametrize('category', ['sale', 'lease'])
async def test_fetch_estates_category(category: str):
    response = await fetch_estates(category=category, limit=1)

    assert response[0].category == category
