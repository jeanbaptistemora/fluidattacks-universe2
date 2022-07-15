from .constants import (
    ALL_STAKEHOLDERS_INDEX_METADATA,
)
from .utils import (
    format_stakeholder,
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
from custom_exceptions import (
    ErrorLoadingStakeholders,
    StakeholderNotFound,
)
from db_model import (
    TABLE,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
)


async def get_all_stakeholders() -> tuple[Stakeholder, ...]:
    primary_key = keys.build_key(
        facet=ALL_STAKEHOLDERS_INDEX_METADATA,
        values={"all": "all"},
    )
    index = TABLE.indexes["gsi_2"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(ALL_STAKEHOLDERS_INDEX_METADATA,),
        table=TABLE,
        index=index,
    )

    if not response.items:
        raise ErrorLoadingStakeholders()

    return tuple(format_stakeholder(item) for item in response.items)


async def _get_stakeholder(*, email: str) -> Stakeholder:
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_metadata"],
        values={"email": email},
    )
    item = await operations.get_item(
        facets=(TABLE.facets["stakeholder_metadata"],),
        key=primary_key,
        table=TABLE,
    )
    if not item:
        raise StakeholderNotFound()

    return format_stakeholder(item)


class StakeholderLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, emails: Iterable[str]
    ) -> tuple[Stakeholder, ...]:
        return await collect(
            tuple(_get_stakeholder(email=email) for email in emails)
        )
