from publisher.publisher import _apply_new_only_filter


def test_apply_new_only_filter_happy_path(fixture_empty_posted_ads_id, fixture_estates_list):
    res = _apply_new_only_filter(fixture_estates_list)

    assert len(res) == 2
