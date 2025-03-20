"""App dataclasses."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Estate:
    """Estate type."""

    id: int
    category: str
    source_name: str
    source_uid: str
    title: str
    layout: str
    address: str
    price: int
    usable_area: int
    district_number: int
    energy_rating: str
    image_url: str
    page_url: str
    updated_at: str


@dataclass
class Invoice:
    """Payment invoice."""

    user_id: int
    price: int
    days: int


@dataclass
class Subscription:
    """User subscription type."""

    _subs_expired_soon_days_threshold = 2

    user_id: int
    expired_at: date

    @property
    def is_active(self) -> bool:
        """Is active subscription."""
        return self.expired_at >= date.today()

    @property
    def is_expired_soon(self) -> bool:
        """Is expired soon subscription."""
        if not self.is_active:
            return False

        expired_days = (self.expired_at - date.today()).days
        return expired_days <= self._subs_expired_soon_days_threshold


@dataclass
class UserFilters:
    """User filters for search new estates."""

    user_id: int
    category: str | None = None
    min_price: int | None = None
    max_price: int | None = None
    layouts: set[str] | None = None
    districts: set[int] | None = None
    enabled: bool = False

    @property
    def is_enabled(self) -> bool:
        """Is enabled filters."""
        return self.enabled

    def is_compatible(self, estate: Estate) -> bool:
        """Is estate item passed by filters."""
        if self.category and estate.category != self.category:
            return False

        if self.min_price and estate.price < self.min_price:  # noqa: WPS531
            return False

        if self.max_price and estate.price > self.max_price:  # noqa: WPS531
            return False

        if self.districts and estate.district_number not in self.districts:  # noqa: WPS531
            return False

        if self.layouts and estate.layout not in self.layouts:  # noqa: WPS531
            return False

        return True


@dataclass
class Price:
    """Price type."""

    cost: int  # XTR currency
    days: int
    title: str
