import pytest
from aiogram import exceptions
from aiogram.methods import SendPhoto
from aiogram.types import BufferedInputFile

from publisher.components import notifications

VIAREALITY_PHOTO_URL = 'https://fra1.digitaloceanspaces.com/viareality/996f0605-9cad-4657-9474-fe34e486a13a_6469'


def _bad_request(message: str) -> exceptions.TelegramBadRequest:
    return exceptions.TelegramBadRequest(method=SendPhoto(chat_id=1, photo='url'), message=message)


async def test_send_estate_happy_path(mocker, fixture_estate_item):
    send_photo_mock = mocker.AsyncMock()

    await notifications.send_estate(send_photo_mock, fixture_estate_item, 'en')

    send_photo_mock.assert_awaited_once()
    assert send_photo_mock.call_args.kwargs['photo'] == fixture_estate_item.image_url


async def test_send_estate_upload_photo_fallback(mocker, fixture_estate_item):
    fixture_estate_item.image_url = VIAREALITY_PHOTO_URL
    send_photo_mock = mocker.AsyncMock(side_effect=[
        _bad_request('Bad Request: failed to get HTTP URL content'),
        None,
    ])

    await notifications.send_estate(send_photo_mock, fixture_estate_item, 'en')

    assert send_photo_mock.await_count == 2
    uploaded_photo = send_photo_mock.call_args.kwargs['photo']
    assert isinstance(uploaded_photo, BufferedInputFile)
    assert uploaded_photo.data.startswith(b'\xff\xd8')


async def test_send_estate_other_bad_request(mocker, fixture_estate_item):
    send_photo_mock = mocker.AsyncMock(side_effect=_bad_request('Bad Request: chat not found'))

    with pytest.raises(exceptions.TelegramBadRequest, match='chat not found'):
        await notifications.send_estate(send_photo_mock, fixture_estate_item, 'en')

    send_photo_mock.assert_awaited_once()


async def test_send_estate_photo_download_failed(mocker, fixture_estate_item):
    fixture_estate_item.image_url = 'https://fra1.digitaloceanspaces.com/viareality/not-exists'
    send_photo_mock = mocker.AsyncMock(side_effect=_bad_request('Bad Request: failed to get HTTP URL content'))

    with pytest.raises(exceptions.TelegramBadRequest, match='failed to get HTTP URL content'):
        await notifications.send_estate(send_photo_mock, fixture_estate_item, 'en')

    send_photo_mock.assert_awaited_once()
