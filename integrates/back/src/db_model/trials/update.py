from .types import (
    TrialMetadataToUpdate,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from db_model import (
    TABLE,
)
from db_model.utils import (
    serialize,
)
from dynamodb import (
    keys,
    operations,
)
import simplejson


async def update_metadata(
    *,
    email: str,
    metadata: TrialMetadataToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    key = keys.build_key(
        facet=TABLE.facets["trial_metadata"],
        values={"all": "all", "email": email},
    )
    item = simplejson.loads(simplejson.dumps(metadata, default=serialize))

    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item=item,
        key=key,
        table=TABLE,
    )
