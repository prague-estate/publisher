from collections import Counter

from publisher import storage
from publisher.subs_downgrade import run


async def test_subs_downgrade_happy_path(fixture_empty_storage):
    storage.renew_subscription(user_id=1, days=3)
    storage.renew_subscription(user_id=2, days=2)
    storage.renew_subscription(user_id=3, days=1)
    storage.renew_subscription(user_id=4, days=-1)

    res = await run()

    assert isinstance(res, Counter)
    assert res['expired soon'] == 2
    assert res['downgraded'] == 1
