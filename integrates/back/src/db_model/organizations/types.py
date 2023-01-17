from datetime import (
    datetime,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.types import (
    Policies,
)
from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
    Optional,
)


class DocumentFile(NamedTuple):
    file_name: str
    modified_date: datetime


class OrganizationDocuments(NamedTuple):
    rut: Optional[DocumentFile] = None
    tax_id: Optional[DocumentFile] = None


class OrganizationPaymentMethods(NamedTuple):
    id: str
    business_name: str
    email: str
    country: str
    state: str
    city: str
    documents: OrganizationDocuments


class OrganizationState(NamedTuple):
    status: OrganizationStateStatus
    modified_by: str
    modified_date: datetime
    pending_deletion_date: Optional[datetime] = None


class OrganizationStandardCompliance(NamedTuple):
    standard_name: str
    compliance_level: Decimal


class OrganizationUnreliableIndicators(NamedTuple):
    covered_authors: Optional[int] = None
    covered_commits: Optional[int] = None
    covered_repositories: Optional[int] = None
    missed_authors: Optional[int] = None
    missed_commits: Optional[int] = None
    missed_repositories: Optional[int] = None
    compliance_level: Optional[Decimal] = None
    compliance_weekly_trend: Optional[Decimal] = None
    estimated_days_to_full_compliance: Optional[Decimal] = None
    standard_compliances: Optional[list[OrganizationStandardCompliance]] = None


class Organization(NamedTuple):
    created_by: str
    created_date: Optional[datetime]
    id: str
    name: str
    policies: Policies
    state: OrganizationState
    country: str
    payment_methods: Optional[list[OrganizationPaymentMethods]] = None
    billing_customer: Optional[str] = None
    vulnerabilities_url: Optional[str] = None


class OrganizationMetadataToUpdate(NamedTuple):
    billing_customer: Optional[str] = None
    payment_methods: Optional[list[OrganizationPaymentMethods]] = None
    vulnerabilities_url: Optional[str] = None


class OrganizationUnreliableIndicatorsToUpdate(NamedTuple):
    covered_authors: Optional[int] = None
    covered_commits: Optional[int] = None
    covered_repositories: Optional[int] = None
    missed_authors: Optional[int] = None
    missed_commits: Optional[int] = None
    missed_repositories: Optional[int] = None
    compliance_level: Optional[Decimal] = None
    compliance_weekly_trend: Optional[Decimal] = None
    estimated_days_to_full_compliance: Optional[Decimal] = None
    standard_compliances: Optional[list[OrganizationStandardCompliance]] = None
