from db_model.organization.constants import (
    DEFAULT_MAX_SEVERITY,
    DEFAULT_MIN_SEVERITY,
)
from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
    Optional,
)


class MaxNumberAcceptations(NamedTuple):
    modified_date: str
    modified_by: str
    max_number_acceptations: int


class Organization(NamedTuple):
    id: str
    name: str
    max_number_acceptations: Optional[MaxNumberAcceptations]
    billing_customer: Optional[str] = None
    pending_deletion_date: Optional[str] = None
    max_acceptance_days: Optional[int] = None
    max_acceptance_severity: Decimal = DEFAULT_MAX_SEVERITY
    min_acceptance_severity: Decimal = DEFAULT_MIN_SEVERITY
    min_breaking_severity: Decimal = DEFAULT_MIN_SEVERITY
    vulnerability_grace_period: Optional[int] = None
