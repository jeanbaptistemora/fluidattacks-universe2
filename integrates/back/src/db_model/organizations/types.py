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
)


class DocumentFile(NamedTuple):
    file_name: str
    modified_date: datetime


class OrganizationDocuments(NamedTuple):
    rut: DocumentFile | None = None
    tax_id: DocumentFile | None = None


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
    pending_deletion_date: datetime | None = None


class OrganizationStandardCompliance(NamedTuple):
    standard_name: str
    compliance_level: Decimal


class OrganizationUnreliableIndicators(NamedTuple):
    covered_authors: int | None = None
    covered_commits: int | None = None
    covered_repositories: int | None = None
    missed_authors: int | None = None
    missed_commits: int | None = None
    missed_repositories: int | None = None
    compliance_level: Decimal | None = None
    compliance_weekly_trend: Decimal | None = None
    estimated_days_to_full_compliance: Decimal | None = None
    standard_compliances: list[OrganizationStandardCompliance] | None = None


class Organization(NamedTuple):
    created_by: str
    created_date: datetime | None
    id: str
    name: str
    policies: Policies
    state: OrganizationState
    country: str
    payment_methods: list[OrganizationPaymentMethods] | None = None
    billing_customer: str | None = None
    vulnerabilities_url: str | None = None


class OrganizationMetadataToUpdate(NamedTuple):
    billing_customer: str | None = None
    payment_methods: list[OrganizationPaymentMethods] | None = None
    vulnerabilities_url: str | None = None


class OrganizationUnreliableIndicatorsToUpdate(NamedTuple):
    covered_authors: int | None = None
    covered_commits: int | None = None
    covered_repositories: int | None = None
    missed_authors: int | None = None
    missed_commits: int | None = None
    missed_repositories: int | None = None
    compliance_level: Decimal | None = None
    compliance_weekly_trend: Decimal | None = None
    estimated_days_to_full_compliance: Decimal | None = None
    standard_compliances: list[OrganizationStandardCompliance] | None = None
