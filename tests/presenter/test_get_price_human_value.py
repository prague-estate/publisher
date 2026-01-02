import pytest

from publisher.components.presenter import get_price_human_value


@pytest.mark.parametrize('payload_price, payload_currency, expected', [
    (0, 'Kč', 'not set'),
    (None, 'Kč', 'not set'),
    (None, None, 'not set'),
    (999, 'Kč/m2', '999 Kč/m2'),
    (1000, '$', '1 000 $'),
    (999999, 'Kč', '999 999 Kč'),
    (1000000, None, '1 000 000 Kč'),
    (13450900, '€', '13 450 900 €'),
])
def test_get_price_human_value(payload_price, payload_currency, expected):
    response = get_price_human_value(payload_price, payload_currency)

    assert response == expected
