import pytest

from publisher.presenter import get_price_human_value


@pytest.mark.parametrize('payload, expected', [
    (0, 'not set'),
    (None, 'not set'),
    (999, '999 Kč'),
    (1000, '1 000 Kč'),
    (999999, '999 999 Kč'),
    (1000000, '1 000 000 Kč'),
    (13450900, '13 450 900 Kč'),
])
def test_get_price_human_value(payload, expected):
    response = get_price_human_value(payload)

    assert response == expected
