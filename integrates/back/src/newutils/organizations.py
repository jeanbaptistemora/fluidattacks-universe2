from db_model.organization.constants import (
    DEFAULT_MAX_SEVERITY,
    DEFAULT_MIN_SEVERITY,
)
from db_model.organization.types import (
    MaxNumberAcceptations,
    Organization,
)
from dynamodb.types import (
    Item,
)
from newutils.datetime import (
    convert_to_iso_str,
)
from newutils.utils import (
    get_key_or_fallback,
)


def format_max_number_acceptations(
    item: list[Item],
) -> MaxNumberAcceptations:
    organizations_max_number_acceptation = item[-1]
    return MaxNumberAcceptations(
        modified_date=(
            convert_to_iso_str(organizations_max_number_acceptation["date"])
        ),
        modified_by=organizations_max_number_acceptation["user"],
        max_number_acceptations=int(
            get_key_or_fallback(
                organizations_max_number_acceptation,
                "max_number_acceptances",
                "max_number_acceptations",
            )
        ),
    )


def format_organization(
    item: Item,
    organization_id: str,
) -> Organization:
    max_number_acceptations = format_max_number_acceptations(
        item["historic_max_number_acceptances"]
        if item.get("historic_max_number_acceptances")
        else item["historic_max_number_acceptations"]
    )
    return Organization(
        id=organization_id.split("#")[1],
        name=item.get("name", ""),
        max_number_acceptations=max_number_acceptations,
        billing_customer=item.get("billing_customer", None),
        pending_deletion_date=(
            convert_to_iso_str(item.get("pending_deletion_date", None))
        ),
        max_acceptance_days=int(item.get("max_acceptance_days", None)),
        max_acceptance_severity=item.get(
            "max_acceptance_severity", DEFAULT_MAX_SEVERITY
        ),
        min_acceptance_severity=item.get(
            "min_acceptance_severity", DEFAULT_MIN_SEVERITY
        ),
        min_breaking_severity=item.get(
            "min_breaking_severity", DEFAULT_MIN_SEVERITY
        ),
        vulnerability_grace_period=int(
            item.get("vulnerability_grace_period", None)
        ),
    )
