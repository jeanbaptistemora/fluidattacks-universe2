from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
)
from db_model.organizations.utils import (
    remove_org_id_prefix,
)
from dynamodb import (
    keys,
)
from dynamodb.operations import (
    batch_delete_item,
    delete_item,
    query,
)
from dynamodb.types import (
    PrimaryKey,
)


async def remove(*, email: str, organization_id: str) -> None:
    email = email.lower().strip()
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_access"],
        values={
            "email": email,
            "id": remove_org_id_prefix(organization_id),
        },
    )

    await delete_item(key=primary_key, table=TABLE)

    historic_key = keys.build_key(
        facet=TABLE.facets["organization_historic_access"],
        values={
            "email": email,
            "id": remove_org_id_prefix(organization_id),
        },
    )
    key_structure = TABLE.primary_key
    response = await query(
        condition_expression=(
            Key(key_structure.partition_key).eq(historic_key.partition_key)
        ),
        facets=(TABLE.facets["organization_historic_access"],),
        table=TABLE,
    )
    await batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item[key_structure.partition_key],
                sort_key=item[key_structure.sort_key],
            )
            for item in response.items
        ),
        table=TABLE,
    )
