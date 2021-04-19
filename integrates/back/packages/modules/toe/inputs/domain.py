# Standard libraries
from typing import (
    Tuple,
)

# Local libraries
from data_containers.toe_inputs import GitRootToeInput
from toe.inputs import dal as toe_inputs_dal


async def add(root_toe_input: GitRootToeInput) -> None:
    await toe_inputs_dal.create(root_toe_input)


async def delete(
    entry_point: str,
    component: str,
    group_name: str
) -> None:
    await toe_inputs_dal.delete(
        entry_point,
        component,
        group_name
    )


async def get_by_group(
    group_name: str
) -> Tuple[GitRootToeInput, ...]:
    return await toe_inputs_dal.get_by_group(group_name)


async def update(root_toe_input: GitRootToeInput) -> None:
    await toe_inputs_dal.update(root_toe_input)
