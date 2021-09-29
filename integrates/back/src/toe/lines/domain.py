from db_model import (
    toe_lines as toe_lines_model,
)
from db_model.toe_lines.types import (
    ToeLines,
)


async def add(toe_lines: ToeLines) -> None:
    await toe_lines_model.add(toe_lines=toe_lines)


async def remove(filename: str, group_name: str, root_id: str) -> None:
    await toe_lines_model.remove(
        filename=filename, group_name=group_name, root_id=root_id
    )


async def update(toe_lines: ToeLines) -> None:
    await toe_lines_model.update(toe_lines=toe_lines)
