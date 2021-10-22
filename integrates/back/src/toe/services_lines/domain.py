from db_model import (
    services_toe_lines as toe_lines_model,
)
from db_model.services_toe_lines.types import (
    ServicesToeLines,
    ServicesToeLinesMetadataToUpdate,
)


async def add(services_toe_lines: ServicesToeLines) -> None:
    await toe_lines_model.add(services_toe_lines=services_toe_lines)


async def remove(filename: str, group_name: str, root_id: str) -> None:
    await toe_lines_model.remove(
        filename=filename, group_name=group_name, root_id=root_id
    )


async def update(
    services_toe_lines: ServicesToeLines, include_risk_level: bool = True
) -> None:
    metadata = ServicesToeLinesMetadataToUpdate(
        comments=services_toe_lines.comments,
        filename=services_toe_lines.filename,
        group_name=services_toe_lines.group_name,
        loc=services_toe_lines.loc,
        modified_commit=services_toe_lines.modified_commit,
        modified_date=services_toe_lines.modified_date,
        root_id=services_toe_lines.root_id,
        tested_date=services_toe_lines.tested_date,
        tested_lines=services_toe_lines.tested_lines,
        sorts_risk_level=services_toe_lines.sorts_risk_level
        if include_risk_level
        else None,
    )
    await toe_lines_model.update_metadata(
        group_name=services_toe_lines.group_name,
        filename=services_toe_lines.filename,
        root_id=services_toe_lines.root_id,
        metadata=metadata,
    )
