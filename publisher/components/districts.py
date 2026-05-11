"""Districts helpers."""
from publisher.components.api_client import fetch_districts
from publisher.components.types import District


async def get_district_names() -> list[str]:
    """Fetch districts and return only names."""
    districts: list[District] = await fetch_districts()
    return sorted([
        district.name
        for district in districts
    ])
