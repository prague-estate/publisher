from publisher.publisher import _apply_new_only_filter
from publisher.storage import mark_as_posted


def test_apply_new_only_filter_happy_path(fixture_empty_posted_ads_id, fixture_estates_list):
    mark_as_posted([fixture_estates_list[0].id])

    res = _apply_new_only_filter(fixture_estates_list)

    assert len(res) == 1
    assert res[0].id == fixture_estates_list[1].id
