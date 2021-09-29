from .types import (
    ToeInput,
)
from .utils import (
    format_toe_input,
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
from dynamodb import (
    keys,
    operations,
)
from dynamodb.model import (
    TABLE,
)
from typing import (
    List,
    Tuple,
)


async def _get_toe_inputs_by_group(group_name: str) -> Tuple[ToeInput, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_toe_input"],
        values={"group_name": group_name},
    )
    key_structure = TABLE.primary_key
    inputs_key = primary_key.sort_key.split("#")[0]
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(inputs_key)
        ),
        facets=(TABLE.facets["root_toe_input"],),
        index=None,
        table=TABLE,
    )
    return tuple(
        format_toe_input(group_name=group_name, item=item) for item in results
    )


class GroupToeInputsLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[ToeInput, ...], ...]:
        return await collect(tuple(map(_get_toe_inputs_by_group, group_names)))
