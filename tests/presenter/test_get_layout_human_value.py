import pytest

from publisher.presenter import _get_layout_human_value


@pytest.mark.parametrize('payload, expected', [
    ('one_kk', '1+kk'),
    ('one_one', '1+1'),
    ('two_kk', '2+kk'),
    ('two_one', '2+1'),
    ('three_kk', '3+kk'),
    ('three_one', '3+1'),
    ('four_kk', '4+kk'),
    ('four_more', '4 & more'),
    ('others', 'unique layout'),
])
def test_get_price_human_value(payload, expected):
    response = _get_layout_human_value(payload)

    assert response == expected
