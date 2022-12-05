from boto3.dynamodb.conditions import (
    Attr,
)
from db_model import (
    TABLE,
)
from db_model.companies.types import (
    CompanyMetadataToUpdate,
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
    domain: str,
    metadata: CompanyMetadataToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    key = keys.build_key(
        facet=TABLE.facets["company_metadata"],
        values={"domain": domain},
    )
    item = simplejson.loads(simplejson.dumps(metadata, default=serialize))

    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item=item,
        key=key,
        table=TABLE,
    )
