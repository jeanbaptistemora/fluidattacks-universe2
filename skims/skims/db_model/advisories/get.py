from .types import (
    Advisory,
)
from .utils import (
    format_advisory,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Tuple,
)


async def _get_advisories(
    *, platform: str, package_name: str
) -> Tuple[Advisory, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["advisories"],
        values={"platform": platform, "pkg_name": package_name},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
        ),
        facets=(TABLE.facets["advisories"],),
        table=TABLE,
    )

    return tuple(format_advisory(item) for item in response.items)
