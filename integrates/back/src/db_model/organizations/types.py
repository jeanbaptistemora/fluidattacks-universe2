from .constants import (
    DEFAULT_MAX_SEVERITY,
    DEFAULT_MIN_SEVERITY,
)
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
    modified_by: str
    modified_date: str
    pending_deletion_date: Optional[str] = None


class OrganizationPolicies(NamedTuple):
    modified_date: str
    modified_by: str
    max_acceptance_days: Optional[int] = None
    max_acceptance_severity: Optional[Decimal] = DEFAULT_MAX_SEVERITY
    max_number_acceptances: Optional[int] = None
    min_acceptance_severity: Optional[Decimal] = DEFAULT_MAX_SEVERITY
    min_breaking_severity: Optional[Decimal] = DEFAULT_MIN_SEVERITY
    vulnerability_grace_period: Optional[int] = None


class OrganizationPoliciesToUpdate(NamedTuple):
    max_acceptance_days: Optional[int] = None
    max_acceptance_severity: Optional[Decimal] = None
    max_number_acceptances: Optional[int] = None
    min_acceptance_severity: Optional[Decimal] = None
    min_breaking_severity: Optional[Decimal] = None
    vulnerability_grace_period: Optional[int] = None


class Organization(NamedTuple):
    id: str
    name: str
    policies: OrganizationPolicies
    state: OrganizationState
    billing_customer: Optional[str] = None


class OrganizationMetadataToUpdate(NamedTuple):
    billing_customer: Optional[str] = None
