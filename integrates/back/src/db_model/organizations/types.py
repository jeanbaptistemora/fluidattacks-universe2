from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.types import (
    Policies,
)
from typing import (
    NamedTuple,
    Optional,
)


class OrganizationPaymentMethods(NamedTuple):
    id: str
    business_name: str
    email: str
    country: str
    state: str
    city: str


class OrganizationState(NamedTuple):
    status: OrganizationStateStatus
    modified_by: str
    modified_date: str
    pending_deletion_date: Optional[str] = None


class Organization(NamedTuple):
    id: str
    name: str
    policies: Policies
    state: OrganizationState
    payment_methods: Optional[list[OrganizationPaymentMethods]] = None
    billing_customer: Optional[str] = None


class OrganizationMetadataToUpdate(NamedTuple):
    billing_customer: Optional[str] = None
    payment_methods: Optional[list[OrganizationPaymentMethods]] = None
