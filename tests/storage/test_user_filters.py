import pytest

from publisher.storage import get_user_filters, update_user_filter


def test_get_user_filters_not_found():
    response = get_user_filters(1)

    assert response.user_id == 1
    assert response.is_enabled is False
    assert response.enabled is False
    assert response.category is None
    assert response.max_price is None


def test_get_user_filters_happy_path():
    update_user_filter(1, category='sale')

    response = get_user_filters(1)

    assert response.user_id == 1
    assert response.is_enabled is False
    assert response.enabled is False
    assert response.category == 'sale'
    assert response.max_price is None


@pytest.mark.parametrize('payload, expected', [
    ('test', 'test'),
    (None, None),
])
def test_update_user_filter_category(payload, expected):
    update_user_filter(1, category=payload)

    response = get_user_filters(1)
    assert getattr(response, 'category') == expected


@pytest.mark.parametrize('payload, expected', [
    (100500, 100500),
    (0, 0),
    (None, None),
])
def test_update_user_filter_max_price(payload, expected):
    update_user_filter(1, max_price=payload)

    response = get_user_filters(1)
    assert getattr(response, 'max_price') == expected


@pytest.mark.parametrize('payload, expected', [
    (True, True),
    (False, False),
    (None, False),
])
def test_update_user_filter_enabled(payload, expected):
    update_user_filter(1, enabled=payload)

    response = get_user_filters(1)
    assert getattr(response, 'enabled') == expected


@pytest.mark.parametrize('payload, expected', [
    (None, None),
    ({21}, {21}),
    ({1, 5, 21}, {1, 5, 21}),
])
def test_update_user_filter_districts(payload, expected):
    update_user_filter(1, districts=payload)

    response = get_user_filters(1)
    assert getattr(response, 'districts') == expected


@pytest.mark.parametrize('payload, expected', [
    (None, None),
    (
        {'1_kk', '1_1', '2_kk', '2_1', '3_kk', '3_1', '4_kk', '4_more', 'others'},
        {'1_kk', '1_1', '2_kk', '2_1', '3_kk', '3_1', '4_kk', '4_more', 'others'},
    ),
    (
        {'2_1', 'others'},
        {'2_1', 'others'},
    ),
])
def test_update_user_filter_layouts(payload, expected):
    update_user_filter(1, layouts=payload)

    response = get_user_filters(1)
    assert getattr(response, 'layouts') == expected
