import pytest

from publisher.components.presenter import get_price_human_value


@pytest.mark.parametrize('payload_price, expected', [
    (0, 'not set'),
    (None, 'not set'),
    (None, 'not set'),
    (999, '999'),
    (1000, '1 000'),
    (999999, '999 999'),
    (1000000, '1 000 000'),
    (13450900, '13 450 900'),
])
def test_get_price_human_value(payload_price, expected):
    response = get_price_human_value(payload_price, 'en')

    assert response == expected
