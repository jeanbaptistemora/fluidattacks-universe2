from .types import (
    Company,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from contextlib import (
    suppress,
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
import simplejson


async def add(*, company: Company) -> None:
    key_structure = TABLE.primary_key
    key = keys.build_key(
        facet=TABLE.facets["company_metadata"],
        values={"domain": company.domain.lower()},
    )
    item = {
        key_structure.partition_key: key.partition_key,
        key_structure.sort_key: key.sort_key,
        **simplejson.loads(simplejson.dumps(company)),
    }

    with suppress(ConditionalCheckFailedException):
        await operations.put_item(
            condition_expression=(
                Attr(key_structure.partition_key).not_exists()
            ),
            facet=TABLE.facets["company_metadata"],
            item=item,
            table=TABLE,
        )