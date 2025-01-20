"""Local storage functions."""
import uuid
from dataclasses import asdict
from datetime import date, timedelta

from redis import Redis  # type: ignore

from publisher.settings import app_settings
from publisher.types import Invoice, Subscription, UserFilters

db_pool: Redis = Redis.from_url(
    app_settings.REDIS_DSN,
    encoding='utf-8',
    decode_responses=True,
)

POSTED_ADS_KEY = 'prague-publisher:posted_ads:id'
TTL_POSTED_ADS = 60 * 60 * 24 * 90  # 3 month  # noqa: WPS432
INVOICE_KEY = 'prague-publisher:invoice:hash'
TTL_INVOICE = 60 * 60  # 1 hour
USER_FILTERS_KEY = 'prague-publisher:user_filters:id'
SUBSCRIPTION_KEY = 'prague-publisher:subscription:id'
SUBSCRIPTIONS_ACTIVE_KEY = 'prague-publisher:subscription:active'


def mark_as_posted(ads_ids: list[int]) -> int:
    """Mark ads as posted."""
    cnt = 0
    for one_id in ads_ids:
        db_pool.set(f'{POSTED_ADS_KEY}:{one_id}', 1, ex=TTL_POSTED_ADS)
        cnt += 1

    return cnt


def is_not_posted_yet(ads_id: int) -> bool:
    """Check what ads was already posted."""
    is_posted = db_pool.exists(f'{POSTED_ADS_KEY}:{ads_id}')

    return not is_posted


def get_user_filters(user_id: int) -> UserFilters:
    """Return user estate filters or default."""
    default_data = asdict(UserFilters(user_id=user_id))
    saved_data: dict | None = db_pool.hgetall(name=f'{USER_FILTERS_KEY}:{user_id}')  # type: ignore

    if not saved_data:
        return UserFilters(
            **default_data,
        )

    if saved_data.get('category') is not None:
        default_data['category'] = saved_data.get('category')

    if saved_data.get('enabled') is not None:
        default_data['enabled'] = bool(int(saved_data.get('enabled')))  # type: ignore

    if saved_data.get('max_cost') is not None:
        default_data['max_cost'] = int(saved_data.get('max_cost'))  # type: ignore

    return UserFilters(
        **default_data,
    )


def update_user_filter(user_id: int, **kwargs: str | int | bool | None) -> None:
    """Update user estate filters."""
    filters_key = f'{USER_FILTERS_KEY}:{user_id}'
    for filter_name, filter_value in kwargs.items():
        if filter_value is None:
            db_pool.hdel(filters_key, filter_name)
            continue

        if isinstance(filter_value, bool):
            filter_value = int(filter_value)

        db_pool.hset(
            name=f'{USER_FILTERS_KEY}:{user_id}',
            key=filter_name,
            value=str(filter_value),
        )


def get_active_subscriptions() -> list[Subscription]:
    """Return active subscriptions."""
    active_subs = []
    for user_id in db_pool.smembers(SUBSCRIPTIONS_ACTIVE_KEY):  # type: ignore
        sub = get_subscription(user_id)
        if sub:
            active_subs.append(sub)
    return active_subs


def get_subscription(user_id: int) -> Subscription | None:
    """Return user subscription if exists."""
    subscription_data: dict | None = db_pool.hgetall(name=f'{SUBSCRIPTION_KEY}:{user_id}')  # type: ignore
    if not subscription_data:
        return None

    return Subscription(
        user_id=int(subscription_data['chat_id']),
        expired_at=date.fromisoformat(subscription_data['expired_at']),
    )


def renew_subscription(user_id: int, days: int) -> Subscription:
    """Create or renew user subscription."""
    renew_period = timedelta(days=days)
    sub = get_subscription(user_id)
    sub_key = f'{SUBSCRIPTION_KEY}:{user_id}'

    if sub and sub.is_active:
        # renew active subscription
        db_pool.hset(
            name=sub_key,
            key='expired_at',
            value=(sub.expired_at + renew_period).isoformat(),
        )

    elif sub:
        # restart subscription
        db_pool.hset(
            name=sub_key,
            key='expired_at',
            value=(date.today() + renew_period).isoformat(),
        )

    else:
        # create new subscription
        db_pool.hset(
            name=sub_key,
            mapping={
                'chat_id': user_id,
                'expired_at': (date.today() + renew_period).isoformat(),
            },
        )

    db_pool.sadd(SUBSCRIPTIONS_ACTIVE_KEY, user_id)

    update_user_filter(user_id, enabled=True)

    return get_subscription(user_id)  # type: ignore


def stop_subscription(user_id: int) -> None:
    """Downgrade user subscription."""
    sub_key = f'{SUBSCRIPTION_KEY}:{user_id}'
    db_pool.hset(
        name=sub_key,
        key='expired_at',
        value=(date.today() - timedelta(days=1)).isoformat(),
    )
    db_pool.srem(SUBSCRIPTIONS_ACTIVE_KEY, user_id)


def create_invoice(
    user_id: int,
    price: int,
    days: int,
) -> str:
    """Create new payment invoice."""
    hash_ = uuid.uuid4().hex
    db_pool.hset(
        name=f'{INVOICE_KEY}:{hash_}',
        mapping={
            'user_id': user_id,
            'price': price,
            'days': days,
        },
    )
    db_pool.expire(f'{INVOICE_KEY}:{hash_}', TTL_INVOICE)
    return hash_


def get_invoice(
    invoice_hash: str,
) -> Invoice | None:
    """Return payment invoice if exists."""
    invoice_data: dict | None = db_pool.hgetall(name=f'{INVOICE_KEY}:{invoice_hash}')  # type: ignore
    if not invoice_data:
        return None

    return Invoice(
        user_id=int(invoice_data['user_id']),
        price=int(invoice_data['price']),
        days=int(invoice_data['days']),
    )


def delete_invoice(
    invoice_hash: str,
) -> None:
    """Invalidate invoice."""
    db_pool.delete(f'{INVOICE_KEY}:{invoice_hash}')
