from .types import (
    Trial,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    TrialRestriction,
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
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson


async def add(*, trial: Trial) -> None:
    key_structure = TABLE.primary_key
    key = keys.build_key(
        facet=TABLE.facets["trial_metadata"],
        values={"all": "all", "email": trial.email},
    )
    item = {
        key_structure.partition_key: key.partition_key,
        key_structure.sort_key: key.sort_key,
        **simplejson.loads(simplejson.dumps(trial, default=serialize)),
    }

    try:
        await operations.put_item(
            condition_expression=(
                Attr(key_structure.partition_key).not_exists()
            ),
            facet=TABLE.facets["trial_metadata"],
            item=item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise TrialRestriction() from ex
