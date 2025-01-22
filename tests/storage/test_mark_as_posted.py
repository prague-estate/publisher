from publisher.storage import is_not_posted_yet, mark_as_posted


def test_mark_as_posted():
    mark_as_posted([1])

    assert is_not_posted_yet(1) is False
    assert is_not_posted_yet(2) is True
