from publisher.components.storage import create_invoice, delete_invoice, get_invoice


def test_create_invoice():
    response = create_invoice(user_id=1, days=1)

    assert len(response) > 10


def test_get_invoice():
    hash_ = create_invoice(user_id=1, days=1)

    response = get_invoice(hash_)

    assert response.user_id == 1
    assert response.days == 1


def test_delete_invoice():
    hash_ = create_invoice(user_id=1, days=1)

    delete_invoice(hash_)

    assert get_invoice(hash_) is None
