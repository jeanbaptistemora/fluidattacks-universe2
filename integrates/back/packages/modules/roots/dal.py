# Standard
from typing import Optional, Tuple

# Local
from dynamodb import model
from dynamodb.types import RootItem

# Constants
ENTITY = 'ROOT'
TABLE_NAME = 'integrates_vms'


async def get_roots(*, group_name: str) -> Tuple[RootItem, ...]:
    roots: Tuple[RootItem, ...] = await model.get_roots(group_name=group_name)

    return roots


async def get_root(
    *,
    group_name: str,
    url: str,
    branch: str
) -> Optional[RootItem]:
    return await model.get_root(
        group_name=group_name,
        url=url,
        branch=branch
    )
