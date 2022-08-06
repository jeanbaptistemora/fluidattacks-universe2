from .constants import (
    ORGANIZATION_ID_PREFIX,
)
from .types import (
    DocumentFile,
    Organization,
    OrganizationDocuments,
    OrganizationMetadataToUpdate,
    OrganizationPaymentMethods,
    OrganizationState,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.types import (
    Policies,
    PoliciesToUpdate,
)
from dynamodb.types import (
    Item,
)
import simplejson as json  # type: ignore


def add_org_id_prefix(organization_id: str) -> str:
    no_prefix_id = remove_org_id_prefix(organization_id)
    return f"{ORGANIZATION_ID_PREFIX}{no_prefix_id}"


def remove_org_id_prefix(organization_id: str) -> str:
    return organization_id.lstrip(ORGANIZATION_ID_PREFIX)


def format_metadata_item(metadata: OrganizationMetadataToUpdate) -> Item:
    item = {
        "billing_customer": metadata.billing_customer,
        "payment_methods": [
            json.loads(json.dumps(payment_method))
            for payment_method in metadata.payment_methods
        ]
        if metadata.payment_methods is not None
        else None,
    }
    return {
        key: None if not value else value
        for key, value in item.items()
        if value is not None
    }


def format_organization(item: Item) -> Organization:
    return Organization(
        billing_customer=item.get("billing_customer"),
        id=add_org_id_prefix(item["id"]),
        name=item["name"],
        payment_methods=format_payment_methods(
            item.get("payment_methods", [])
        ),
        policies=format_policies(item["policies"]),
        state=format_state(item["state"]),
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
        modified_date=policies["modified_date"],
        modified_by=policies["modified_by"],
        vulnerability_grace_period=int(policies["vulnerability_grace_period"])
        if "vulnerability_grace_period" in policies
        else None,
    )


def format_policies_item(
    modified_by: str,
    modified_date: str,
    policies: PoliciesToUpdate,
) -> Item:
    item = {
        "modified_by": modified_by,
        "modified_date": modified_date,
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
        modified_date=state["modified_date"],
        pending_deletion_date=state.get("pending_deletion_date"),
    )


def format_documents(documents: Item) -> OrganizationDocuments:
    return OrganizationDocuments(
        rut=DocumentFile(
            file_name=documents["rut"]["file_name"],
            modified_date=documents["rut"]["modified_date"],
        )
        if documents.get("rut")
        else None,
        tax_id=DocumentFile(
            file_name=documents["tax_id"]["file_name"],
            modified_date=documents["tax_id"]["modified_date"],
        )
        if documents.get("tax_id")
        else None,
    )
