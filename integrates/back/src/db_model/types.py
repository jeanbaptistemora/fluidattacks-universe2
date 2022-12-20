from .constants import (
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
    Optional,
)


class CodeLanguage(NamedTuple):
    language: str
    loc: int


class Policies(NamedTuple):
    modified_date: datetime
    modified_by: str
    max_acceptance_days: Optional[int] = None
    max_acceptance_severity: Optional[Decimal] = DEFAULT_MAX_SEVERITY
    max_number_acceptances: Optional[int] = None
    min_acceptance_severity: Optional[Decimal] = DEFAULT_MIN_SEVERITY
    min_breaking_severity: Optional[Decimal] = DEFAULT_MIN_SEVERITY
    vulnerability_grace_period: Optional[int] = None


class PoliciesToUpdate(NamedTuple):
    max_acceptance_days: Optional[int] = None
    max_acceptance_severity: Optional[Decimal] = None
    max_number_acceptances: Optional[int] = None
    min_acceptance_severity: Optional[Decimal] = None
    min_breaking_severity: Optional[Decimal] = None
    vulnerability_grace_period: Optional[int] = None
