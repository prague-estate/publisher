import asyncio

import pytest

from publisher.storage import mark_as_posted, db_pool
from publisher.types import Estate


@pytest.fixture(scope='function')
def event_loop():
    yield asyncio.get_event_loop()


@pytest.fixture()
def fixture_estate_item():
    yield Estate(
        id=1,
        category='sale',
        source_name='sreality',
        source_uid='11',
        title='title 1',
        address='address',
        price=100500,
        usable_area=53,
        district_number=5005,
        energy_rating='G',
        image_url='https://d18-a.sdn.cz/d_18/c_img_QJ_J5/kMPBBm.jpeg?fl=res',
        page_url='https://www.sreality.cz/detail/prodej/byt/2+kk/praha-liben-pod-labutkou/3788997196',
        updated_at='Tue, 05 Nov 2024 07:57:50 GMT',
    )


@pytest.fixture()
def fixture_one_more_estate_item():
    yield Estate(
        id=2,
        category='sale',
        source_name='sreality',
        source_uid='33',
        title='title 2',
        address='address',
        price=23232,
        usable_area=53,
        district_number=5005,
        energy_rating='F',
        image_url='https://d18-a.sdn.cz/d_18/c_img_QJ_J5/kMPBBm.jpeg?fl=res',
        page_url='https://www.sreality.cz/detail/prodej/byt/3+kk/praha-smichov-ke-koulce/1464591692',
        updated_at='Tue, 05 Nov 2024 07:57:50 GMT',
    )


@pytest.fixture()
def fixture_estates_list(fixture_estate_item, fixture_one_more_estate_item):
    yield [
        fixture_estate_item,
        fixture_one_more_estate_item,
    ]


@pytest.fixture()
def fixture_empty_posted_ads_id():
    db_pool.flushdb()
    yield
    db_pool.flushdb()


@pytest.fixture()
def fixture_prefilled_posted_ads_id(fixture_empty_posted_ads_id) -> list[int]:
    ads_ids = [1, 2, 3]
    mark_as_posted(ads_ids)
    yield ads_ids
