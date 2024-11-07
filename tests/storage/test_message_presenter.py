from publisher.publisher import _message_presenter


def test_message_presenter_smoke(fixture_estate_item):
    res = _message_presenter(fixture_estate_item)

    assert isinstance(res, str)


