import pytest

from publisher.api import fetch_estates


async def test_fetch_estates_contract():
    response = await fetch_estates(category='sale', limit=2)

    assert 'title' in response[0]
    assert 'category' in response[0]
    assert 'source_name' in response[0]
    assert 'source_uid' in response[0]


@pytest.mark.parametrize('limit', [0, 1, 2])
async def test_fetch_estates_limit(limit: int):
    response = await fetch_estates(category='sale', limit=limit)

    assert len(response) == limit


@pytest.mark.parametrize('category', ['sale', 'lease'])
async def test_fetch_estates_category(category: str):
    response = await fetch_estates(category=category, limit=1)

    assert response[0]['category'] == category
