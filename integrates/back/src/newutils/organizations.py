from db_model.organization.constants import (
    DEFAULT_MAX_SEVERITY,
    DEFAULT_MIN_SEVERITY,
)
from db_model.organization.types import (
    Organization,
    OrganizationMaxNumberAcceptations,
)
from dynamodb.types import (
    Item,
)
from newutils.utils import (
    get_key_or_fallback,
)


def organization_max_number_acceptations(
    item: Item,
) -> OrganizationMaxNumberAcceptations:
    return OrganizationMaxNumberAcceptations(
        modified_date=item["date"],
        modified_by=item["user"],
        max_number_acceptations=get_key_or_fallback(
            item,
            "max_number_acceptances",
            "max_number_acceptations",
        ),
    )


def format_organization(
    item: Item,
    organization_id: str,
) -> Organization:
    return Organization(
        id=organization_id,
        name=item["name"],
        billing_customer=item.get("billing_customer", None),
        pending_deletion_date=item.get("pending_deletion_date", None),
        max_acceptance_days=item.get("max_acceptance_days", None),
        max_acceptance_severity=item.get(
            "max_acceptance_severity", DEFAULT_MAX_SEVERITY
        ),
        min_acceptance_severity=item.get(
            "min_acceptance_severity", DEFAULT_MIN_SEVERITY
        ),
        min_breaking_severity=item.get(
            "min_breaking_severity", DEFAULT_MIN_SEVERITY
        ),
        vulnerability_grace_period=item.get(
            "vulnerability_grace_period", None
        ),
        organization_max_number_acceptations=(
            organization_max_number_acceptations(
                get_key_or_fallback(
                    item,
                    "historic_max_number_acceptances",
                    "historic_max_number_acceptations",
                ),
            ),
        ),
    )
