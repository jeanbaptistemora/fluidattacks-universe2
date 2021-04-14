# Standard libraries
from typing import (
    Tuple,
)

# Local libraries
from data_containers.toe_inputs import GitRootToeInput
from toe.inputs import dal as toe_inputs_dal


async def get_by_group(
    group_name: str
) -> Tuple[GitRootToeInput, ...]:
    return await toe_inputs_dal.get_by_group(group_name)
