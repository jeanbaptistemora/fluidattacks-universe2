from .constants import (
    PATCH_SRC,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)


async def remove(
    *, platform: str, pkg_name: str, advisory_id: str, source: str = PATCH_SRC
) -> None:
    primary_key = keys.build_key(
        facet=TABLE.facets["advisories"],
        values={
            "platform": platform,
            "pkg_name": pkg_name,
            "id": advisory_id,
            "src": source,
        },
    )
    await operations.delete_item(key=primary_key, table=TABLE)
