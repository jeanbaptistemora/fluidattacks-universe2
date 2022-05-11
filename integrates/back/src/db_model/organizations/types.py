from db_model.organizations.enums import (
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
    status: OrganizationStateStatus
    modified_by: Optional[str] = None
    modified_date: Optional[str] = None
    pending_deletion_date: Optional[str] = None


class OrganizationPolicies(NamedTuple):
    max_acceptance_days: Optional[int] = None
    max_acceptance_severity: Optional[Decimal] = None
    max_number_acceptances: Optional[int] = None
    min_acceptance_severity: Optional[Decimal] = None
    min_breaking_severity: Optional[Decimal] = None
    modified_date: Optional[str] = None
    modified_by: Optional[str] = None
    vulnerability_grace_period: Optional[int] = None


class Organization(NamedTuple):
    id: str
    name: str
    policies: OrganizationPolicies
    state: OrganizationState
    billing_customer: Optional[str] = None
