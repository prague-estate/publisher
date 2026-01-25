import base64
import hashlib
import json
import logging
from decimal import Decimal

import requests

from publisher.settings import app_settings

PROVIDER_URL = 'https://api.heleket.com/v1/payment'

logger = logging.getLogger(__file__)


def create_invoice(
    order_id: str,
    amount_usdt: Decimal,
) -> str | None:
    payload = {
        'amount': str(amount_usdt),
        'currency': 'USDT',
        'order_id': order_id,
        'is_payment_multiple': False,
        'url_callback': '{0}/{1}'.format(
            app_settings.HELEKET_WEBHOOK_CALLBACK_HOST,
            'webhook',
        ),
        'url_return': app_settings.BOT_LINK,
        'url_success': app_settings.BOT_LINK,
    }
    headers = {
        'merchant': app_settings.HELEKET_MERCHANT_ID,
        'sign': _generate_sign(payload),
    }
    try:
        response = requests.post(
            url=PROVIDER_URL,
            json=payload,
            headers=headers,
        ).json()
        logger.info('heleket response {0} by request {1}'.format(response, payload))
        invoice_data = response['result']
    except (requests.RequestException, KeyError) as exc:
        logger.warning('heleket request error {0}'.format(exc))
        return None

    return invoice_data['url']


def _generate_sign(payload: dict) -> str:
    payload = json.dumps(payload).encode('utf-8')  # type: ignore
    payload64 = base64.b64encode(payload)  # type: ignore
    return hashlib.md5(payload64 + app_settings.HELEKET_API_KEY.encode('utf-8')).hexdigest()
