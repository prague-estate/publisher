from publisher.storage import is_not_posted_yet


def test_is_not_posted_yet_happy_path(fixture_prefilled_posted_ads_id: list[int]):
    for ads_id in fixture_prefilled_posted_ads_id:
        assert is_not_posted_yet(ads_id) is False


def test_is_not_posted_yet_not_found():
    assert is_not_posted_yet(1) is True
