from datetime import timedelta, date

from publisher.storage import renew_subscription, get_user_filters, stop_subscription, get_subscription, \
    get_active_subscriptions


def test_get_active_subscriptions(fixture_empty_storage):
    renew_subscription(user_id=1, days=1)
    renew_subscription(user_id=2, days=1)
    stop_subscription(user_id=1)

    response = get_active_subscriptions()

    assert len(response) == 1
    assert response[0].user_id == 2


def test_get_subscription(fixture_empty_storage):
    renew_subscription(user_id=1, days=1)

    found = get_subscription(user_id=1)
    not_found = get_subscription(user_id=2)

    assert found.is_active is True
    assert not_found is None


def test_stop_subscription(fixture_empty_storage):
    renew_subscription(user_id=1, days=1)

    stop_subscription(user_id=1)

    response = get_subscription(user_id=1)
    assert response.is_active is False


def test_renew_subscription_create_new(fixture_empty_storage):
    response = renew_subscription(user_id=1, days=1)

    assert response.is_active is True
    assert response.is_expired_soon is True
    assert response.expired_at == date.today() + timedelta(days=1)
    assert get_user_filters(user_id=1).is_enabled is True


def test_renew_subscription_renew(fixture_empty_storage):
    renew_subscription(user_id=1, days=1)

    response = renew_subscription(user_id=1, days=8)

    assert response.is_active is True
    assert response.expired_at == date.today() + timedelta(days=9)
    assert get_user_filters(user_id=1).is_enabled is True


def test_renew_subscription_restart(fixture_empty_storage):
    renew_subscription(user_id=1, days=1)
    stop_subscription(user_id=1)

    response = renew_subscription(user_id=1, days=8)

    assert response.is_active is True
    assert response.expired_at == date.today() + timedelta(days=8)
    assert get_user_filters(user_id=1).is_enabled is True
