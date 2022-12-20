from .constants import (
    ORGANIZATION_ID_PREFIX,
)
from .types import (
    DocumentFile,
    Organization,
    OrganizationDocuments,
    OrganizationMetadataToUpdate,
    OrganizationPaymentMethods,
    OrganizationStandardCompliance,
    OrganizationState,
    OrganizationUnreliableIndicators,
    OrganizationUnreliableIndicatorsToUpdate,
)
from datetime import (
    datetime,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.types import (
    Policies,
    PoliciesToUpdate,
)
from db_model.utils import (
    get_as_utc_iso_format,
    serialize,
)
from dynamodb.types import (
    Item,
)
import simplejson as json


def add_org_id_prefix(organization_id: str) -> str:
    no_prefix_id = remove_org_id_prefix(organization_id)
    return f"{ORGANIZATION_ID_PREFIX}{no_prefix_id}"


def remove_org_id_prefix(organization_id: str) -> str:
    return organization_id.lstrip(ORGANIZATION_ID_PREFIX)


def format_metadata_item(metadata: OrganizationMetadataToUpdate) -> Item:
    item = {
        "billing_customer": metadata.billing_customer,
        "payment_methods": [
            json.loads(json.dumps(payment_method, default=serialize))
            for payment_method in metadata.payment_methods
        ]
        if metadata.payment_methods is not None
        else None,
        "vulnerabilities_url": metadata.vulnerabilities_url,
    }
    return {
        key: None if not value else value
        for key, value in item.items()
        if value is not None
    }


def format_organization(item: Item) -> Organization:
    return Organization(
        created_by=item.get("created_by", ""),
        created_date=datetime.fromisoformat(item["created_date"])
        if item.get("created_date")
        else None,
        billing_customer=item.get("billing_customer"),
        country=item.get("country"),
        id=add_org_id_prefix(item["id"]),
        name=item["name"],
        payment_methods=format_payment_methods(
            item.get("payment_methods", [])
        ),
        policies=format_policies(item["policies"]),
        state=format_state(item["state"]),
        vulnerabilities_url=item.get("vulnerabilities_url", None),
    )


def format_payment_methods(
    payment_methods: list[Item],
) -> list[OrganizationPaymentMethods]:
    return [
        OrganizationPaymentMethods(
            id=payment_method.get("id", ""),
            business_name=payment_method.get("business_name", ""),
            documents=format_documents(payment_method["documents"]),
            email=payment_method.get("email", ""),
            country=payment_method.get("country", ""),
            state=payment_method.get("state", ""),
            city=payment_method.get("city", ""),
        )
        for payment_method in payment_methods
    ]


def format_policies(policies: Item) -> Policies:
    return Policies(
        max_acceptance_days=int(policies["max_acceptance_days"])
        if "max_acceptance_days" in policies
        else None,
        max_acceptance_severity=policies.get("max_acceptance_severity"),
        max_number_acceptances=int(policies["max_number_acceptances"])
        if "max_number_acceptances" in policies
        else None,
        min_acceptance_severity=policies.get("min_acceptance_severity"),
        min_breaking_severity=policies.get("min_breaking_severity"),
        modified_date=datetime.fromisoformat(policies["modified_date"]),
        modified_by=policies["modified_by"],
        vulnerability_grace_period=int(policies["vulnerability_grace_period"])
        if "vulnerability_grace_period" in policies
        else None,
    )


def format_policies_item(
    modified_by: str,
    modified_date: datetime,
    policies: PoliciesToUpdate,
) -> Item:
    item = {
        "modified_by": modified_by,
        "modified_date": get_as_utc_iso_format(modified_date),
        "max_acceptance_days": policies.max_acceptance_days,
        "max_acceptance_severity": policies.max_acceptance_severity,
        "min_acceptance_severity": policies.min_acceptance_severity,
        "min_breaking_severity": policies.min_breaking_severity,
        "vulnerability_grace_period": policies.vulnerability_grace_period,
        "max_number_acceptances": policies.max_number_acceptances,
    }

    return {key: value for key, value in item.items() if value is not None}


def format_state(state: Item) -> OrganizationState:
    return OrganizationState(
        status=OrganizationStateStatus[state["status"]],
        modified_by=state["modified_by"],
        modified_date=datetime.fromisoformat(state["modified_date"]),
        pending_deletion_date=datetime.fromisoformat(
            state["pending_deletion_date"]
        )
        if state.get("pending_deletion_date")
        else None,
    )


def format_documents(documents: Item) -> OrganizationDocuments:
    return OrganizationDocuments(
        rut=DocumentFile(
            file_name=documents["rut"]["file_name"],
            modified_date=datetime.fromisoformat(
                documents["rut"]["modified_date"]
            ),
        )
        if documents.get("rut")
        else None,
        tax_id=DocumentFile(
            file_name=documents["tax_id"]["file_name"],
            modified_date=datetime.fromisoformat(
                documents["tax_id"]["modified_date"]
            ),
        )
        if documents.get("tax_id")
        else None,
    )


def format_standard_compliance(item: Item) -> OrganizationStandardCompliance:
    return OrganizationStandardCompliance(
        standard_name=item["standard_name"],
        compliance_level=item["compliance_level"],
    )


def format_standard_compliance_item(
    standard_compliance: OrganizationStandardCompliance,
) -> Item:
    return {
        "standard_name": standard_compliance.standard_name,
        "compliance_level": standard_compliance.compliance_level,
    }


def format_unreliable_indicators(
    item: Item,
) -> OrganizationUnreliableIndicators:
    return OrganizationUnreliableIndicators(
        compliance_level=item.get("compliance_level"),
        compliance_weekly_trend=item.get("compliance_weekly_trend"),
        estimated_days_to_full_compliance=item.get(
            "estimated_days_to_full_compliance"
        ),
        standard_compliances=[
            format_standard_compliance(standard_compliance)
            for standard_compliance in item["standard_compliances"]
        ]
        if "standard_compliances" in item
        else None,
        missed_repositories=item.get("missed_repositories", 0),
        covered_commits=item.get("covered_commits", 0),
        missed_commits=item.get("missed_commits", 0),
        covered_repositories=item.get("covered_repositories", 0),
        missed_authors=item.get("missed_authors", 0),
        covered_authors=item.get("covered_authors", 0),
    )


def format_unreliable_indicators_item(
    indicators: OrganizationUnreliableIndicators,
) -> Item:
    return {
        "compliance_level": indicators.compliance_level,
        "compliance_weekly_trend": indicators.compliance_weekly_trend,
        "estimated_days_to_full_compliance": (
            indicators.estimated_days_to_full_compliance
        ),
        "standard_compliances": [
            format_standard_compliance_item(standard_compliance)
            for standard_compliance in indicators.standard_compliances
        ]
        if indicators.standard_compliances is not None
        else None,
    }


def format_unreliable_indicators_item_to_update(
    indicators: OrganizationUnreliableIndicatorsToUpdate,
) -> Item:
    item = {
        "compliance_level": indicators.compliance_level,
        "compliance_weekly_trend": indicators.compliance_weekly_trend,
        "estimated_days_to_full_compliance": (
            indicators.estimated_days_to_full_compliance
        ),
        "standard_compliances": [
            format_standard_compliance_item(standard_compliance)
            for standard_compliance in indicators.standard_compliances
        ]
        if indicators.standard_compliances is not None
        else None,
        "missed_repositories": indicators.missed_repositories,
        "covered_commits": indicators.covered_commits,
        "missed_commits": indicators.missed_commits,
        "covered_repositories": indicators.covered_repositories,
        "missed_authors": indicators.missed_authors,
        "covered_authors": indicators.covered_authors,
    }

    return {key: value for key, value in item.items() if value is not None}
