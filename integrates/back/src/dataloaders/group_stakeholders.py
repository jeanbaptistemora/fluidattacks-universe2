from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
    Tuple,
)
from users import (
    domain as users_domain,
)


class GroupStakeholdersLoader(DataLoader):
    """Batches load calls within the same execution fragment."""

    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[List[Dict[str, Any]], ...]:
        return cast(
            Tuple[List[Dict[str, Any]], ...],
            await collect(
                tuple(
                    users_domain.get_group_stakeholders(group_name)
                    for group_name in group_names
                )
            ),
        )
