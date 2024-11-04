import pytest

from publisher.storage import is_not_posted_yet


@pytest.mark.parametrize("test_input,expected", [(1, False), (2, False), (3, False), (4, True)])
async def test_is_not_posted_yet_happy_path(test_input, expected, fixture_prefilled_posted_ads_id):
    assert await is_not_posted_yet(test_input) == expected
