from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from data_containers.toe_inputs import (
    GitRootToeInput,
)
from toe.inputs import (
    domain as toe_inputs_domain,
)
from typing import (
    List,
    Tuple,
)


async def get_group_toe_inputs(
    *, group_name: str
) -> Tuple[GitRootToeInput, ...]:
    group_toe_inputs: Tuple[
        GitRootToeInput, ...
    ] = await toe_inputs_domain.get_by_group(group_name)
    return group_toe_inputs


class GroupToeInputsLoader(DataLoader):
    """Batches load calls within the same execution fragment."""

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, group_names: List[str]
    ) -> Tuple[Tuple[GitRootToeInput, ...], ...]:
        return tuple(
            await collect(
                get_group_toe_inputs(group_name=group_name)
                for group_name in group_names
            )
        )
