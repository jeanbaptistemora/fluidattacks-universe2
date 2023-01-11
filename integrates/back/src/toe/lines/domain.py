from .types import (
    ToeLinesAttributesToAdd,
    ToeLinesAttributesToUpdate,
)
from custom_exceptions import (
    InvalidToeLinesAttackAt,
    InvalidToeLinesAttackedLines,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model import (
    toe_lines as toe_lines_model,
)
from db_model.roots.types import (
    Root,
)
from db_model.toe_lines.types import (
    ToeLines,
    ToeLinesMetadataToUpdate,
    ToeLinesState,
)
from newutils import (
    datetime as datetime_utils,
)
from newutils.validations import (
    validate_commit_hash_deco,
    validate_email_address_deco,
    validate_field_length,
    validate_sanitized_csv_input,
    validate_sanitized_csv_input_deco,
)
from roots.validations import (
    validate_active_root_deco,
    validate_git_root_deco,
)
import simplejson as json
from toe.lines.constants import (
    CHECKED_FILES,
)
from toe.lines.utils import (
    get_filename_extension,
)
from toe.lines.validations import (
    validate_loc_deco,
    validate_modified_date_deco,
)
from toe.utils import (
    get_has_vulnerabilities,
)
from typing import (
    Optional,
)


def _get_optional_be_present_until(
    be_present: bool,
) -> Optional[datetime]:
    return datetime_utils.get_utc_now() if be_present is False else None


def _assign_attacked_lines(
    filename: str,
    loc: int,
    modified_date: datetime,
    attacked_at: Optional[datetime],
    attacked_lines: int,
) -> int:
    if get_filename_extension(filename) in CHECKED_FILES:
        return loc
    if attacked_at and modified_date and attacked_at <= modified_date:
        return attacked_lines
    return 0


@validate_loc_deco("loc")
@validate_modified_date_deco("modified_date")
def _validate_assign_attacked_lines(
    filename: str,
    loc: int,
    modified_date: datetime,
    attacked_at: datetime,
    attacked_lines: int,
) -> int:
    return _assign_attacked_lines(
        filename=filename,
        loc=loc,
        modified_date=modified_date,
        attacked_at=attacked_at,
        attacked_lines=attacked_lines,
    )


def _assign_state() -> ToeLinesState:
    return ToeLinesState(
        modified_by="machine@fluidattacks.com",
        modified_date=datetime_utils.get_utc_now(),
    )


@validate_email_address_deco("seen_first_time_by")
def _validate_assign_state(seen_first_time_by: str) -> ToeLinesState:
    return ToeLinesState(
        modified_by=seen_first_time_by,
        modified_date=datetime_utils.get_utc_now(),
    )


def _assign_toe_lines(  # pylint: disable=too-many-arguments
    attributes: ToeLinesAttributesToAdd,
    last_author: str,
    last_commit: str,
    attacked_lines: int,
    filename: str,
    group_name: str,
    root: Root,
    state: ToeLinesState,
) -> ToeLines:
    be_present_until = (
        attributes.be_present_until
        or _get_optional_be_present_until(attributes.be_present)
    )
    first_attack_at = attributes.first_attack_at or attributes.attacked_at
    has_vulnerabilities = get_has_vulnerabilities(
        attributes.be_present, attributes.has_vulnerabilities
    )
    return ToeLines(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        attacked_lines=attacked_lines,
        be_present=attributes.be_present,
        be_present_until=be_present_until,
        comments=attributes.comments,
        filename=filename,
        first_attack_at=first_attack_at,
        has_vulnerabilities=has_vulnerabilities,
        group_name=group_name,
        last_author=last_author,
        last_commit=last_commit,
        loc=attributes.loc,
        modified_date=attributes.modified_date,
        root_id=root.id,
        seen_at=attributes.seen_at or datetime_utils.get_utc_now(),
        seen_first_time_by=attributes.seen_first_time_by,
        sorts_risk_level=attributes.sorts_risk_level,
        state=state,
    )


@validate_sanitized_csv_input_deco(["last_author", "filename"])
@validate_email_address_deco("last_author")
@validate_commit_hash_deco("last_commit")
@validate_git_root_deco("root")
@validate_active_root_deco("root")
def _validate_assign_toe_lines(  # pylint: disable=too-many-arguments
    attributes: ToeLinesAttributesToAdd,
    last_author: str,
    last_commit: str,
    attacked_lines: int,
    filename: str,
    group_name: str,
    root: Root,
    state: ToeLinesState,
) -> ToeLines:
    return _assign_toe_lines(
        attributes=attributes,
        last_author=last_author,
        last_commit=last_commit,
        attacked_lines=attacked_lines,
        filename=filename,
        group_name=group_name,
        root=root,
        state=state,
    )


async def add(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    group_name: str,
    root_id: str,
    filename: str,
    attributes: ToeLinesAttributesToAdd,
    is_moving_toe_lines: bool = False,
) -> None:
    root: Root = await loaders.root.load((group_name, root_id))
    state = _assign_state()
    if is_moving_toe_lines is False:
        if attributes.seen_first_time_by is not None:
            state = _validate_assign_state(
                seen_first_time_by=attributes.seen_first_time_by
            )

        attacked_lines = _validate_assign_attacked_lines(
            filename=filename,
            loc=attributes.loc,
            modified_date=attributes.modified_date,
            attacked_at=attributes.attacked_at,
            attacked_lines=attributes.attacked_lines,
        )
        print(root)
        toe_lines = _validate_assign_toe_lines(
            attributes=attributes,
            last_author=attributes.last_author,
            last_commit=attributes.last_commit,
            attacked_lines=attacked_lines,
            filename=filename,
            group_name=group_name,
            root=root,
            state=state,
        )
    else:
        attacked_lines = _assign_attacked_lines(
            filename=filename,
            loc=attributes.loc,
            modified_date=attributes.modified_date,
            attacked_at=attributes.attacked_at,
            attacked_lines=attributes.attacked_lines,
        )
        toe_lines = _assign_toe_lines(
            attributes=attributes,
            last_author=attributes.last_author,
            last_commit=attributes.last_commit,
            attacked_lines=attacked_lines,
            filename=filename,
            group_name=group_name,
            root=root,
            state=state,
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
    is_moving_toe_lines: bool = False,
) -> None:
    if (  # pylint: disable=too-many-boolean-expressions
        not is_moving_toe_lines
        and (
            attributes.attacked_at is not None
            and current_value.attacked_at is not None
        )
        and (
            attributes.attacked_at <= current_value.attacked_at
            or attributes.attacked_at > datetime_utils.get_utc_now()
            or attributes.attacked_at < current_value.seen_at
        )
    ):
        raise InvalidToeLinesAttackAt()

    loc = attributes.loc if attributes.loc is not None else current_value.loc
    if (
        is_moving_toe_lines is False
        and attributes.attacked_lines is not None
        and not (0 <= attributes.attacked_lines <= loc)
    ):
        raise InvalidToeLinesAttackedLines()

    if is_moving_toe_lines is False and attributes.comments is not None:
        validate_field_length(attributes.comments, 200)
        validate_sanitized_csv_input(attributes.comments)

    last_attacked_at = attributes.attacked_at or current_value.attacked_at
    last_modified_date = (
        attributes.modified_date or current_value.modified_date
    )
    first_attack_at = None
    if attributes.first_attack_at is not None:
        first_attack_at = attributes.first_attack_at
    elif not current_value.first_attack_at and attributes.attacked_at:
        first_attack_at = attributes.attacked_at

    if get_filename_extension(current_value.filename) in CHECKED_FILES:
        attacked_lines = loc
    elif (
        attributes.attacked_lines != 0
        and last_attacked_at
        and last_modified_date <= last_attacked_at
    ):
        attacked_lines = min(
            attributes.attacked_lines or current_value.attacked_lines, loc
        )
    else:
        attacked_lines = 0

    be_present_until = (
        None
        if attributes.be_present is None
        else _get_optional_be_present_until(attributes.be_present)
    )
    current_be_present = (
        current_value.be_present
        if attributes.be_present is None
        else attributes.be_present
    )
    has_vulnerabilities = (
        get_has_vulnerabilities(
            current_be_present, attributes.has_vulnerabilities
        )
        if attributes.has_vulnerabilities is not None
        or attributes.be_present is not None
        else None
    )
    metadata = ToeLinesMetadataToUpdate(
        attacked_at=attributes.attacked_at,
        attacked_by=attributes.attacked_by,
        attacked_lines=attacked_lines,
        be_present=attributes.be_present,
        be_present_until=be_present_until,
        comments=attributes.comments,
        last_author=attributes.last_author,
        first_attack_at=first_attack_at,
        has_vulnerabilities=has_vulnerabilities,
        loc=attributes.loc,
        last_commit=attributes.last_commit,
        modified_date=attributes.modified_date,
        seen_at=attributes.seen_at,
        sorts_risk_level=attributes.sorts_risk_level,
        sorts_risk_level_date=attributes.sorts_risk_level_date
        if attributes.sorts_risk_level_date is not None
        else None,
        clean_be_present_until=attributes.be_present is not None
        and be_present_until is None,
        sorts_suggestions=json.loads(json.dumps(attributes.sorts_suggestions))
        if attributes.sorts_suggestions is not None
        else None,
        state=ToeLinesState(
            modified_by=attributes.attacked_by
            if attributes.attacked_by
            else "machine@fluidattacks.com",
            modified_date=datetime_utils.get_utc_now(),
        ),
    )
    await toe_lines_model.update_metadata(
        current_value=current_value,
        metadata=metadata,
    )
