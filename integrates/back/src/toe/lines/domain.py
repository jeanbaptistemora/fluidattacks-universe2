from .types import (
    ToeLinesAttributesToAdd,
    ToeLinesAttributesToUpdate,
)
from custom_exceptions import (
    InvalidToeLinesAttackAt,
    InvalidToeLinesAttackedLines,
    ToeLinesNotPresent,
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


def _get_optional_be_present_until(
    be_present: bool,
) -> Optional[datetime]:
    return datetime_utils.get_utc_now() if be_present is False else None


async def add(
    group_name: str,
    root_id: str,
    filename: str,
    attributes: ToeLinesAttributesToAdd,
) -> None:
    attacked_lines = (
        attributes.attacked_lines
        if attributes.attacked_at
        and attributes.modified_date
        and attributes.attacked_at <= attributes.modified_date
        else 0
    )
    be_present_until = (
        attributes.be_present_until
        or _get_optional_be_present_until(attributes.be_present)
    )
    first_attack_at = attributes.attacked_at
    toe_lines = ToeLines(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        attacked_lines=attacked_lines,
        be_present=attributes.be_present,
        be_present_until=be_present_until,
        comments=attributes.comments,
        commit_author=attributes.commit_author,
        filename=filename,
        first_attack_at=first_attack_at,
        group_name=group_name,
        loc=attributes.loc,
        modified_commit=attributes.modified_commit,
        modified_date=attributes.modified_date,
        root_id=root_id,
        seen_at=attributes.seen_at or datetime_utils.get_utc_now(),
        sorts_risk_level=attributes.sorts_risk_level,
    )
    await toe_lines_model.add(toe_lines=toe_lines)


async def remove(
    group_name: str,
    root_id: str,
    filename: str,
) -> None:
    await toe_lines_model.remove(
        group_name=group_name, root_id=root_id, filename=filename
    )


async def update(
    current_value: ToeLines,
    attributes: ToeLinesAttributesToUpdate,
) -> None:
    if (
        attributes.is_moving_toe_lines is False
        and attributes.be_present is None
        and current_value.be_present is False
    ):
        raise ToeLinesNotPresent()

    if (
        attributes.is_moving_toe_lines is False
        and attributes.attacked_at is not None
        and current_value.attacked_at is not None
    ):
        if (
            attributes.attacked_at <= current_value.attacked_at
            or attributes.attacked_at > datetime_utils.get_utc_now()
        ):
            raise InvalidToeLinesAttackAt()

    if (
        attributes.is_moving_toe_lines is False
        and attributes.attacked_lines is not None
        and not (1 <= attributes.attacked_lines <= current_value.loc)
    ):
        raise InvalidToeLinesAttackedLines()

    last_attacked_at = attributes.attacked_at or current_value.attacked_at
    last_modified_date = (
        attributes.modified_date or current_value.modified_date
    )
    first_attack_at = (
        attributes.first_attack_at
        if attributes.first_attack_at is not None
        else attributes.attacked_at
        if not current_value.first_attack_at and attributes.attacked_at
        else None
    )
    attacked_lines = (
        attributes.attacked_lines or current_value.attacked_lines
        if attributes.attacked_lines != 0
        and last_attacked_at
        and last_modified_date <= last_attacked_at
        else 0
    )
    be_present_until = (
        None
        if attributes.be_present is None
        else _get_optional_be_present_until(attributes.be_present)
    )
    seen_at = (
        attributes.seen_at
        if attributes.seen_at is None
        else attributes.seen_at or current_value.seen_at
    )
    metadata = ToeLinesMetadataToUpdate(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        attacked_lines=attacked_lines,
        be_present=attributes.be_present,
        be_present_until=be_present_until,
        comments=attributes.comments,
        commit_author=attributes.commit_author,
        first_attack_at=first_attack_at,
        loc=attributes.loc,
        modified_commit=attributes.modified_commit,
        modified_date=attributes.modified_date,
        seen_at=seen_at,
        sorts_risk_level=attributes.sorts_risk_level,
        clean_be_present_until=attributes.be_present is not None
        and be_present_until is None,
    )
    await toe_lines_model.update_metadata(
        current_value=current_value,
        metadata=metadata,
    )
