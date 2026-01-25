from publisher.components.storage import create_invoice


def test_purchase_webhook_happy_path(test_client):
    invoice_hash = create_invoice(user_id=1, days=1)

    response = test_client.post('/webhook', json={'order_id': invoice_hash, 'status': 'paid'})

    assert response.status_code == 200
