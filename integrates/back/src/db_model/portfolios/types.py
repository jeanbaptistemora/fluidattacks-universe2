from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
    Optional,
)


class PortfolioUnreliableIndicators(NamedTuple):
    last_closing_date: Optional[int] = None
    max_open_severity: Optional[Decimal] = None
    max_severity: Optional[Decimal] = None
    mean_remediate: Optional[Decimal] = None
    mean_remediate_critical_severity: Optional[Decimal] = None
    mean_remediate_high_severity: Optional[Decimal] = None
    mean_remediate_low_severity: Optional[Decimal] = None
    mean_remediate_medium_severity: Optional[Decimal] = None


class Portfolio(NamedTuple):
    id: str
    groups: set[str]
    organization_name: str
    unreliable_indicators: PortfolioUnreliableIndicators
