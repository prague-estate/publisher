import asyncio
import logging
from http import HTTPStatus
from typing import Any

from aiogram import exceptions, Bot
from flask import Flask, abort, request

from publisher.components import presenter, storage, translation
from publisher.components.notifications import send_logs_notification
from publisher.components.types import Invoice, Subscription
from publisher.settings import app_settings

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


@app.route('/webhook', methods=['POST'])
def purchase_webhook() -> Any:
    webhook_request = request.json
    user_ip = _get_user_ip()
    app.logger.info('webhook: received {0} from {1}'.format(webhook_request, user_ip))

    if user_ip != app_settings.HELEKET_WEBHOOK_IP:
        app.logger.warning('webhook: invalid ip {0}'.format(user_ip))
        return abort(HTTPStatus.BAD_REQUEST)

    invoice = storage.get_invoice(webhook_request.get('order_id', 'not-found'))
    app.logger.info('webhook: invoice found {0}'.format(invoice))
    if not invoice:
        app.logger.warning('webhook: invoice not found')
        return abort(HTTPStatus.BAD_REQUEST)

    if webhook_request.get('status') not in {'paid', 'paid_over'}:
        app.logger.warning('webhook: payment not success {0}'.format(webhook_request.get('status')))
        return {'status': 'unknown status {0}'.format(webhook_request.get('status'))}

    storage.delete_invoice(webhook_request.get('order_id'))
    sub: Subscription = storage.renew_subscription(
        user_id=invoice.user_id,
        days=invoice.days,
    )

    asyncio.run(_apply_invoice(invoice, sub))
    app.logger.info('webhook: applied')
    return {'status': 'OK'}


async def _apply_invoice(invoice: Invoice, sub: Subscription) -> None:
    await _send_payment_notification_to_user(invoice.user_id, sub)
    await send_logs_notification('crypto payment accepted {0}'.format(invoice))


def _get_user_ip() -> str | None:
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr


async def _send_payment_notification_to_user(user_id: int, sub: Subscription) -> None:
    settings = storage.get_user_settings(user_id)
    async with Bot(app_settings.BOT_TOKEN) as bot_instance:
        try:
            await bot_instance.send_message(
                chat_id=user_id,
                text=translation.get_i8n_text('payment.accepted', settings.lang).format(sub.expired_at.isoformat()),
                reply_markup=presenter.get_main_menu(user_id),
            )
        except (exceptions.TelegramBadRequest, exceptions.TelegramForbiddenError) as exc:
            app.logger.warning('sent notification to user error: {0}'.format(exc))
