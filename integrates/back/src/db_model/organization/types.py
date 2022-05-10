from db_model.organization.constants import (
    DEFAULT_MAX_SEVERITY,
    DEFAULT_MIN_SEVERITY,
)
from db_model.organization.enums import (
    OrganizationStateStatus,
)
from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
    Optional,
)


class OrganizationState(NamedTuple):
    modified_date: str
    modified_by: str
    status: OrganizationStateStatus


class OrganizationPolicies(NamedTuple):
    modified_date: str
    modified_by: str
    max_number_acceptations: int


class Organization(NamedTuple):
    id: str
    name: str
    billing_customer: Optional[str] = None
    max_acceptance_days: Optional[int] = None
    max_acceptance_severity: Decimal = DEFAULT_MAX_SEVERITY
    max_number_acceptations: Optional[int] = None
    min_acceptance_severity: Decimal = DEFAULT_MIN_SEVERITY
    min_breaking_severity: Decimal = DEFAULT_MIN_SEVERITY
    pending_deletion_date: Optional[str] = None
    policies: Optional[OrganizationPolicies] = None
    state: Optional[OrganizationState] = None
    vulnerability_grace_period: Optional[int] = None
