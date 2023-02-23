from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
)


class PortfolioUnreliableIndicators(NamedTuple):
    last_closing_date: int | None = None
    max_open_severity: Decimal | None = None
    max_severity: Decimal | None = None
    mean_remediate: Decimal | None = None
    mean_remediate_critical_severity: Decimal | None = None
    mean_remediate_high_severity: Decimal | None = None
    mean_remediate_low_severity: Decimal | None = None
    mean_remediate_medium_severity: Decimal | None = None


class Portfolio(NamedTuple):
    id: str
    groups: set[str]
    organization_name: str
    unreliable_indicators: PortfolioUnreliableIndicators


class PortfolioRequest(NamedTuple):
    organization_name: str
    portfolio_id: str
