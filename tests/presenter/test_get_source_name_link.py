import pytest

from publisher.components.presenter import _get_source_name_link


@pytest.mark.parametrize('payload, expected', [
    ('sreality', 'sreality.cz'),
    ('bezrealitky', 'bezrealitky.cz'),
    ('svoboda', 'svoboda-williams.com'),
    ('expats', 'expats.cz'),
    ('idnes', 'reality.idnes.cz'),
    ('engelvoelkers', 'engelvoelkers.com'),
    ('remax', 'remax-czech.cz'),
    ('ulovdomov', 'ulovdomov.cz'),
])
def test_get_source_name_link(payload, expected):
    response = _get_source_name_link(payload)

    assert response == expected
