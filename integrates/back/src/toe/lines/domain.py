from db_model import (
    toe_lines as toe_lines_model,
)
from db_model.toe_lines.types import (
    ServicesToeLines,
    ServicesToeLinesMetadataToUpdate,
)


async def add(toe_lines: ServicesToeLines) -> None:
    await toe_lines_model.add(toe_lines=toe_lines)


async def remove(filename: str, group_name: str, root_id: str) -> None:
    await toe_lines_model.remove(
        filename=filename, group_name=group_name, root_id=root_id
    )


async def update(
    toe_lines: ServicesToeLines, include_risk_level: bool = True
) -> None:
    metadata = ServicesToeLinesMetadataToUpdate(
        comments=toe_lines.comments,
        filename=toe_lines.filename,
        group_name=toe_lines.group_name,
        loc=toe_lines.loc,
        modified_commit=toe_lines.modified_commit,
        modified_date=toe_lines.modified_date,
        root_id=toe_lines.root_id,
        tested_date=toe_lines.tested_date,
        tested_lines=toe_lines.tested_lines,
        sorts_risk_level=toe_lines.sorts_risk_level
        if include_risk_level
        else None,
    )
    await toe_lines_model.update_metadata(
        group_name=toe_lines.group_name,
        filename=toe_lines.filename,
        root_id=toe_lines.root_id,
        metadata=metadata,
    )
