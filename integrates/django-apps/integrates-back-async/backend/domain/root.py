# Standard
from typing import List

# Third party
# None

# Local
from backend.dal import root as root_dal
from backend.typing import Root


async def get_roots_by_group(group_name: str) -> List[Root]:
    roots = await root_dal.get_roots_by_group(group_name)

    return [
        Root(id=root['sk'], kind=root['kind'])
        for root in roots
    ]
