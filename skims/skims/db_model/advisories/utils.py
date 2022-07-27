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


def format_advisory_item(advisory: Advisory) -> Item:
    return {
        "associated_advisory": advisory.associated_advisory,
        "package_name": advisory.package_name,
        "package_manager": advisory.package_manager,
        "vulnerable_version": advisory.vulnerable_version,
        "severity": advisory.severity,
        "source": advisory.source,
    }
