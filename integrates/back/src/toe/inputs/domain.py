from db_model import (
    toe_inputs as toe_inputs_model,
)
from db_model.toe_inputs.types import (
    ToeInput,
)


async def add(toe_input: ToeInput) -> None:
    await toe_inputs_model.add(toe_input=toe_input)


async def remove(entry_point: str, component: str, group_name: str) -> None:
    await toe_inputs_model.remove(
        entry_point=entry_point, component=component, group_name=group_name
    )


async def update(toe_input: ToeInput) -> None:
    await toe_inputs_model.update(toe_input=toe_input)
