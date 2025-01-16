from publisher.storage import mark_as_posted, is_not_posted_yet


def test_mark_as_posted(fixture_empty_storage):
    mark_as_posted([1])

    assert is_not_posted_yet(1) is False
    assert is_not_posted_yet(2) is True
