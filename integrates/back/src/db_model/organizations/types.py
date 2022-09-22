# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    modified_date: str


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
    modified_date: str
    pending_deletion_date: Optional[str] = None


class OrganizationUnreliableIndicators(NamedTuple):
    non_compliance_level: Optional[Decimal] = None


class Organization(NamedTuple):
    country: str
    id: str
    name: str
    policies: Policies
    state: OrganizationState
    payment_methods: Optional[list[OrganizationPaymentMethods]] = None
    billing_customer: Optional[str] = None
    vulnerabilities_url: Optional[str] = None


class OrganizationMetadataToUpdate(NamedTuple):
    billing_customer: Optional[str] = None
    payment_methods: Optional[list[OrganizationPaymentMethods]] = None
    vulnerabilities_url: Optional[str] = None
