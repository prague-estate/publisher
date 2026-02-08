import logging

_has_stop_request: bool = False

logger = logging.getLogger(__file__)


def exit_request(*args, message: str = '', **kwargs) -> None:  # type: ignore
    """Stop signal handler."""
    global _has_stop_request  # noqa: WPS420, WPS442
    _has_stop_request = True  # noqa: WPS122, WPS442
    logger.info('force exit {0}'.format(message))


def has_exit_request() -> bool:
    """Get True when exit was requested."""
    return _has_stop_request
