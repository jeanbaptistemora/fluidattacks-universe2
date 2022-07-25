from .types import (
    Advisory,
)
from dynamodb.types import (
    Item,
)


def format_advisory(item: Item) -> Advisory:
    return Advisory(
        associated_advisory=item["associated_advisory"],
        package_name=item["package_name"],
        package_manager=item["package_manager"],
        vulnerable_version=item["vulnerable_version"],
        severity=item["severity"],
        source=item["source"],
    )
