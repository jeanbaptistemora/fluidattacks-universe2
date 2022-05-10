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
    historic_policies: Optional[OrganizationPolicies] = None
    historic_status: Optional[OrganizationState] = None
    billing_customer: Optional[str] = None
    pending_deletion_date: Optional[str] = None
    max_acceptance_days: Optional[int] = None
    max_number_acceptations: Optional[int] = None
    max_acceptance_severity: Decimal = DEFAULT_MAX_SEVERITY
    min_acceptance_severity: Decimal = DEFAULT_MIN_SEVERITY
    min_breaking_severity: Decimal = DEFAULT_MIN_SEVERITY
    vulnerability_grace_period: Optional[int] = None
