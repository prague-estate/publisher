import pytest

from publisher.components.translation import get_i8n_text


def test_get_i8n_text_happy_path():
    assert get_i8n_text('about', 'en')


def test_get_i8n_text_language():
    assert get_i8n_text('menu.settings', 'en') != get_i8n_text('menu.settings', 'ru')


def test_get_i8n_text_not_found():
    with pytest.raises(KeyError):
        assert get_i8n_text('invalid', 'ru')
