from .types import (
    ToeLinesAttributesToAdd,
    ToeLinesAttributesToUpdate,
)
from db_model import (
    toe_lines as toe_lines_model,
)
from db_model.toe_lines.types import (
    ToeLines,
    ToeLinesMetadataToUpdate,
)
from newutils import (
    datetime as datetime_utils,
)


async def add(
    group_name: str,
    root_id: str,
    filename: str,
    attributes: ToeLinesAttributesToAdd,
) -> None:
    toe_lines = ToeLines(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        attacked_lines=attributes.attacked_lines,
        be_present=attributes.be_present,
        comments=attributes.comments,
        filename=filename,
        first_attack_at=attributes.first_attack_at,
        group_name=group_name,
        loc=attributes.loc,
        modified_commit=attributes.modified_commit,
        modified_date=attributes.modified_date,
        root_id=root_id,
        seen_at=datetime_utils.get_iso_date(),
        sorts_risk_level=attributes.sorts_risk_level,
    )
    await toe_lines_model.add(toe_lines=toe_lines)


async def update(
    current_value: ToeLines,
    group_name: str,
    root_id: str,
    filename: str,
    attributes: ToeLinesAttributesToUpdate,
) -> None:
    metadata = ToeLinesMetadataToUpdate(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        attacked_lines=attributes.attacked_lines,
        be_present=attributes.be_present,
        comments=attributes.comments,
        first_attack_at=attributes.first_attack_at,
        loc=attributes.loc,
        modified_commit=attributes.modified_commit,
        modified_date=attributes.modified_date,
        seen_at=attributes.seen_at,
        sorts_risk_level=attributes.sorts_risk_level,
    )
    await toe_lines_model.update_metadata(
        current_value=current_value,
        group_name=group_name,
        filename=filename,
        root_id=root_id,
        metadata=metadata,
    )
