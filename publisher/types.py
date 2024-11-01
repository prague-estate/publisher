"""App dataclasses."""

from dataclasses import dataclass


@dataclass
class Estate:
    """Estate dataclass."""

    id: int
    category: str
    source_name: str
    source_uid: str
    title: str
    address: str
    price: int
    usable_area: int
    district_number: int
    energy_rating: str
    image_url: str
    page_url: str
    updated_at: str
