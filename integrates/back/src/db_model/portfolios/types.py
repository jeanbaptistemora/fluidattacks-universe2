from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
)


class PortfolioUnreliableIndicators(NamedTuple):
    last_closing_date: int
    max_open_severity: Decimal
    max_severity: Decimal
    mean_remediate: Decimal
    mean_remediate_critical_severity: Decimal
    mean_remediate_high_severity: Decimal
    mean_remediate_low_severity: Decimal
    mean_remediate_medium_severity: Decimal


class Portfolio(NamedTuple):
    id: str
    groups: set[str]
    organization_id: str
    unreliable_indicators: PortfolioUnreliableIndicators
