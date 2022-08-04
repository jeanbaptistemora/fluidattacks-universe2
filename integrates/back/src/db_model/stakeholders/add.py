from .constants import (
    ALL_STAKEHOLDERS_INDEX_METADATA,
)
from .types import (
    Stakeholder,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    StakeholderAlreadyCreated,
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


async def add(*, stakeholder: Stakeholder) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={
            "email": stakeholder.email,
        },
    )
    gsi_2_key = keys.build_key(
        facet=ALL_STAKEHOLDERS_INDEX_METADATA,
        values={
            "all": "all",
            "email": stakeholder.email,
        },
    )
    item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        **json.loads(json.dumps(stakeholder)),
    }

    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=TABLE.facets["stakeholder_metadata"],
            item=item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise StakeholderAlreadyCreated.new() from ex
