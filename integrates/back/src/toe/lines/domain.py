from .types import (
    ToeLinesAttributesToAdd,
    ToeLinesAttributesToUpdate,
)
from datetime import (
    datetime,
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
from typing import (
    Optional,
)


def _get_be_present_until(
    be_present: bool,
) -> str:
    return datetime_utils.get_iso_date() if be_present is False else ""


def _get_optional_be_present_until(
    optional_be_present: Optional[bool],
) -> Optional[str]:
    return (
        None
        if optional_be_present is None
        else _get_be_present_until(optional_be_present)
    )


async def add(
    group_name: str,
    root_id: str,
    filename: str,
    attributes: ToeLinesAttributesToAdd,
) -> None:
    be_present_until = _get_be_present_until(attributes.be_present)
    toe_lines = ToeLines(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        attacked_lines=attributes.attacked_lines,
        be_present=attributes.be_present,
        be_present_until=be_present_until,
        comments=attributes.comments,
        commit_author=attributes.commit_author,
        filename=filename,
        first_attack_at=attributes.first_attack_at,
        group_name=group_name,
        is_deactivated=False,
        loc=attributes.loc,
        modified_commit=attributes.modified_commit,
        modified_date=attributes.modified_date,
        root_id=root_id,
        seen_at=attributes.seen_at or datetime_utils.get_iso_date(),
        sorts_risk_level=attributes.sorts_risk_level,
    )
    await toe_lines_model.add(toe_lines=toe_lines)


async def update(
    current_value: ToeLines,
    attributes: ToeLinesAttributesToUpdate,
) -> None:
    attacked_at = attributes.attacked_at or current_value.attacked_at
    modified_date = attributes.modified_date or current_value.modified_date
    attacked_lines = (
        attributes.attacked_lines or current_value.attacked_lines
        if attacked_at
        and datetime.fromisoformat(modified_date)
        <= datetime.fromisoformat(attacked_at)
        else 0
    )
    be_present_until = _get_optional_be_present_until(attributes.be_present)
    metadata = ToeLinesMetadataToUpdate(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        attacked_lines=attacked_lines,
        be_present=attributes.be_present,
        be_present_until=be_present_until,
        comments=attributes.comments,
        commit_author=attributes.commit_author,
        first_attack_at=attributes.first_attack_at,
        is_deactivated=attributes.is_deactivated,
        loc=attributes.loc,
        modified_commit=attributes.modified_commit,
        modified_date=attributes.modified_date,
        seen_at=attributes.seen_at,
        sorts_risk_level=attributes.sorts_risk_level,
    )
    await toe_lines_model.update_metadata(
        current_value=current_value,
        metadata=metadata,
    )
