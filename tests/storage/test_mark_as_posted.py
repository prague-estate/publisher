from publisher.storage import mark_as_posted, is_not_posted_yet


async def test_mark_as_posted(fixture_empty_posted_ads_id):
    ads_ids = [1, 2, 3]
    await mark_as_posted(ads_ids)

    for id_item in ads_ids:
        assert await is_not_posted_yet(id_item) is False
