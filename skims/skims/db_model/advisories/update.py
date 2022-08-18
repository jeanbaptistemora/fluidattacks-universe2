from .types import (
    Advisory,
)
from .utils import (
    format_advisory_item,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)


async def update(
    *,
    advisory: Advisory,
) -> None:
    advisory_key = keys.build_key(
        facet=TABLE.facets["advisories"],
        values={
            "platform": advisory.package_manager,
            "pkg_name": advisory.package_name,
            "src": advisory.source,
            "id": advisory.associated_advisory,
        },
    )
    advisory_item = format_advisory_item(advisory)
    await operations.update_item(
        item=advisory_item,
        key=advisory_key,
        table=TABLE,
    )
    print(f"Updated ( {advisory_key.sort_key} )")
