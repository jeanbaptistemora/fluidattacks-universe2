from .constants import (
    DEFAULT_INACTIVITY_PERIOD,
    DEFAULT_MAX_SEVERITY,
    DEFAULT_MIN_SEVERITY,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
)


class CodeLanguage(NamedTuple):
    language: str
    loc: int


class Policies(NamedTuple):
    modified_date: datetime
    modified_by: str
    inactivity_period: int | None = DEFAULT_INACTIVITY_PERIOD
    max_acceptance_days: int | None = None
    max_acceptance_severity: Decimal | None = DEFAULT_MAX_SEVERITY
    max_number_acceptances: int | None = None
    min_acceptance_severity: Decimal | None = DEFAULT_MIN_SEVERITY
    min_breaking_severity: Decimal | None = None
    vulnerability_grace_period: int | None = None


class PoliciesToUpdate(NamedTuple):
    inactivity_period: int | None = None
    max_acceptance_days: int | None = None
    max_acceptance_severity: Decimal | None = None
    max_number_acceptances: int | None = None
    min_acceptance_severity: Decimal | None = None
    min_breaking_severity: Decimal | None = None
    vulnerability_grace_period: int | None = None
