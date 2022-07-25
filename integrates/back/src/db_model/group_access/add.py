from .types import (
    GroupAccess,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    AccessAlreadyCreated,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json  # type: ignore


async def add(*, group_access: GroupAccess) -> None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["group_access"],
        values={
            "email": group_access.email,
            "name": group_access.group_name,
        },
    )
    item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        **json.loads(json.dumps(group_access)),
    }

    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=TABLE.facets["group_access"],
            item=item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise AccessAlreadyCreated.new() from ex
