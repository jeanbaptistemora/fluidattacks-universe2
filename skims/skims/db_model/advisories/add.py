# pylint: disable=import-error
from .types import (
    Advisory,
)
from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    AdvisoryAlreadyCreated,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
import simplejson as json  # type: ignore


async def add(*, advisory: Advisory) -> None:
    items = []
    key_structure = TABLE.primary_key
    advisory_key = keys.build_key(
        facet=TABLE.facets["advisories"],
        values={
            "platform": advisory.package_manager,
            "pkg_name": advisory.package_name,
            "src": advisory.source,
            "id": advisory.associated_advisory,
        },
    )

    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(advisory_key.partition_key)
        ),
        facets=(TABLE.facets["advisories"],),
        limit=1,
        table=TABLE,
    )
    if response.items:
        raise AdvisoryAlreadyCreated.new()

    advisory_item = {
        key_structure.partition_key: advisory_key.partition_key,
        key_structure.sort_key: advisory_key.sort_key,
        **json.loads(json.dumps(advisory)),
    }
    items.append(advisory_item)

    await operations.batch_put_item(items=tuple(items), table=TABLE)
