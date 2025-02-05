from publisher.presenter import _get_estate_description


def test_get_estate_description_smoke(fixture_estate_item):
    res = _get_estate_description(fixture_estate_item)

    assert isinstance(res, str)


