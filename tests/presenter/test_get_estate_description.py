import pytest

from publisher.components.presenter import _get_estate_description
from publisher.settings import app_settings


@pytest.mark.parametrize('lang', app_settings.ENABLED_LANGUAGES)
def test_get_estate_description_smoke(fixture_estate_item, lang):
    res = _get_estate_description(fixture_estate_item, lang)

    assert isinstance(res, str)


