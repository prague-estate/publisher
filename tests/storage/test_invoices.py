from publisher.storage import get_invoice, create_invoice, delete_invoice


def test_create_invoice(fixture_empty_storage):
    response = create_invoice(user_id=1, price=17, days=1)

    assert len(response) > 10


def test_get_invoice(fixture_empty_storage):
    hash_ = create_invoice(user_id=1, price=17, days=1)

    response = get_invoice(hash_)

    assert response.user_id == 1
    assert response.price == 17
    assert response.days == 1


def test_delete_invoice(fixture_empty_storage):
    hash_ = create_invoice(user_id=1, price=17, days=1)

    delete_invoice(hash_)

    assert get_invoice(hash_) is None
