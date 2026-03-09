"""Telegram bot handlers."""
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link

from publisher import handlers
from publisher.components import presenter, storage, translation
from publisher.components.notifications import send_logs_notification
from publisher.settings import app_settings

logger = logging.getLogger(__file__)

bot_instance = Bot(app_settings.BOT_TOKEN)
dp = Dispatcher(storage=RedisStorage.from_url(app_settings.REDIS_DSN))
handlers.init(dp)


@dp.message(CommandStart(deep_link=True, ignore_case=True))
@dp.message(Command('start', ignore_case=True))
async def start(message: Message, command: CommandObject) -> None:
    """Apply promo trial if exists."""
    promo = str(command.args).strip().lower()
    logger.info(f'Start {promo=}')
    promo_days: int | None = app_settings.PROMO_CODES.get(promo)

    if message.from_user and message.from_user.language_code in app_settings.ENABLED_LANGUAGES:
        lang = message.from_user.language_code
    else:
        lang = app_settings.ENABLED_LANGUAGES[0]
    logger.info('set user lang to {0} {1}'.format(
        message.from_user,
        lang,
    ))
    storage.update_user_settings(user_id=message.chat.id, lang=lang)

    if promo_days and not storage.has_used_trial(message.chat.id, promo):
        logger.info('apply promo code')
        sub = storage.renew_subscription(
            user_id=message.chat.id,
            days=promo_days,
        )
        storage.mark_used_trial(message.chat.id, promo)

        await message.answer(  # type: ignore
            text=translation.get_i8n_text('payment.accepted', lang).format(sub.expired_at.isoformat()),
        )
        await send_logs_notification('trial applied "{0}" {1}'.format(
            promo,
            message.chat.id,
        ))

    actual_sub = storage.get_subscription(message.chat.id)
    if actual_sub and actual_sub.is_active:
        await message.answer(  # type: ignore
            text=translation.get_i8n_text('start.set_filters', lang),
            reply_markup=presenter.get_main_menu(message.chat.id),
        )

    else:
        await message.answer(  # type: ignore
            text=translation.get_i8n_text('start.subscribe_first', lang),
            reply_markup=presenter.get_main_menu(message.chat.id),
        )


@dp.message(Command('support'))
@dp.message(Command('paysupport'))
@dp.message(F.text.in_(translation.get_by('menu.about')))
async def about(message: Message) -> None:
    """About project."""
    logger.info('About')
    settings = storage.get_user_settings(message.chat.id)

    await message.answer(
        text=translation.get_i8n_text('about', settings.lang),
        reply_markup=presenter.get_main_menu(message.chat.id),
    )


@dp.message(F.text.in_(translation.get_by('menu.admin')))
async def admin_info(message: Message) -> None:
    """Show info for admins."""
    logger.info('Admin info')

    if not app_settings.is_admin(message.chat.id):
        logger.error('not by admin request!')
        return

    response_messages = [
        'Available promo links',
    ]

    response_messages += [
        '[{0}]({1}) for {2} days'.format(
            code,
            await create_start_link(bot_instance, code),
            days,
        )
        for code, days in app_settings.PROMO_CODES.items()
    ]

    response_messages += [
        '',
        'Active subs: {0}'.format(len(storage.get_active_subscriptions())),
    ]

    await message.answer(
        text='\n'.join(response_messages),
        reply_markup=presenter.get_main_menu(message.chat.id),
        parse_mode='Markdown',
    )


@dp.message(F.text.in_(translation.get_by('menu.filters')))
async def user_filters(message: Message) -> None:
    """User filters setup."""
    logger.info('User filters')
    settings = storage.get_user_settings(message.chat.id)

    await message.answer(
        text=translation.get_i8n_text('filters.description', settings.lang),
        reply_markup=presenter.get_filters_menu(message.chat.id),
    )


@dp.message(F.text.in_(translation.get_by('menu.settings')))
async def user_settings(message: Message) -> None:
    """User settings setup."""
    logger.info('User settings')
    settings = storage.get_user_settings(message.chat.id)

    await message.answer(
        text=translation.get_i8n_text('settings.description', settings.lang),
        reply_markup=presenter.get_settings_menu(message.chat.id),
    )


@dp.message(F.text.in_(
    translation.get_by('menu.subscription.inactive') | translation.get_by('menu.subscription.active'),
))
async def user_subscription(message: Message) -> None:
    """Subscription info."""
    logger.info('Subscription')
    settings = storage.get_user_settings(message.chat.id)

    sub = storage.get_subscription(message.chat.id)
    if sub and sub.is_active:
        text = translation.get_i8n_text('subscription.active', settings.lang).format(sub.expired_at.isoformat())
    else:
        text = translation.get_i8n_text('subscription.inactive', settings.lang)

    await message.answer(
        text=text,
        reply_markup=presenter.get_prices_menu(message.chat.id),
    )


@dp.message()
async def error_handler(message: Message) -> None:
    """Handle stale  and unknown buttons."""
    logger.info('Error handler')
    settings = storage.get_user_settings(message.chat.id)

    await message.answer(
        text=translation.get_i8n_text('error.unknown_button', settings.lang),
        reply_markup=presenter.get_main_menu(message.chat.id),
    )


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG if app_settings.DEBUG else logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    asyncio.run(dp.start_polling(bot_instance))
