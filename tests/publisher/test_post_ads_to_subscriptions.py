from publisher.publisher import _post_ads_to_subscriptions
from publisher.storage import renew_subscription, update_user_filter


async def test_post_ads_to_subscriptions_subs_not_exists(fixture_empty_storage, fixture_estate_item):
    res = await _post_ads_to_subscriptions(
        [fixture_estate_item],
        [],
    )

    assert res == 0


async def test_post_ads_to_subscriptions_subs_not_compatible(fixture_empty_storage, fixture_estate_item):
    sub = renew_subscription(user_id=1, days=1)
    update_user_filter(user_id=1, enabled=False)

    res = await _post_ads_to_subscriptions(
        [fixture_estate_item],
        [sub],
    )

    assert res == 0


async def test_post_ads_to_subscriptions_happy_path(fixture_empty_storage, fixture_estate_item):
    sub = renew_subscription(user_id=1, days=1)

    res = await _post_ads_to_subscriptions(
        [fixture_estate_item],
        [sub],
    )

    assert res == 1
