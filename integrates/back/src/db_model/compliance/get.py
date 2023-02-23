from .types import (
    ComplianceUnreliableIndicators,
)
from .utils import (
    format_unreliable_indicators,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from collections.abc import (
    Iterable,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)


async def _get_compliance_unreliable_indicators() -> (
    ComplianceUnreliableIndicators
):
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["compliance_unreliable_indicators"],
        values={},
    )
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).eq(primary_key.sort_key)
        ),
        facets=(TABLE.facets["compliance_unreliable_indicators"],),
        table=TABLE,
    )
    if not response.items:
        return ComplianceUnreliableIndicators()

    return format_unreliable_indicators(response.items[0])


class ComplianceUnreliableIndicatorsLoader(
    DataLoader[str, ComplianceUnreliableIndicators]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, ids: Iterable[str]
    ) -> list[ComplianceUnreliableIndicators]:
        return list(
            await collect(
                tuple(_get_compliance_unreliable_indicators() for _ in ids)
            )
        )
