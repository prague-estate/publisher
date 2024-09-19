"""Local storage functions."""


async def mark_as_posted(ads_hashes: list[str]) -> int:
    """Mark ads as posted."""
    # todo impl
    # todo use TTL for auto-cleanup after 3 months
    # todo test
    return 0


async def is_already_posted(ads_hash: str) -> bool:
    """Check what ads was already posted."""
    # todo impl
    # todo test
    return False
