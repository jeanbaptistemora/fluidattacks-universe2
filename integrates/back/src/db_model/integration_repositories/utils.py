from .types import (
    OrganizationIntegrationRepository,
)
from datetime import (
    datetime,
)
from db_model.organizations.utils import (
    add_org_id_prefix,
)
from dynamodb.types import (
    Item,
)


def format_organization_integration_repository(
    item: Item,
) -> OrganizationIntegrationRepository:
    return OrganizationIntegrationRepository(
        id=item["sk"],
        organization_id=add_org_id_prefix(item["pk"]),
        branch=item["branch"],
        last_commit_date=datetime.fromisoformat(item["last_commit_date"])
        if item.get("last_commit_date")
        else None,
        url=item["url"],
        commit_count=int(item.get("commit_count", 0)),
    )
