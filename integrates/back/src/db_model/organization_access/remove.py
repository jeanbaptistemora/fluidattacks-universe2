from .utils import (
    remove_org_id_prefix,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
)
from dynamodb.operations import (
    delete_item,
)


async def remove(*, email: str, organization_id: str) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_access"],
        values={
            "email": email,
            "id": remove_org_id_prefix(organization_id),
        },
    )

    await delete_item(key=primary_key, table=TABLE)
