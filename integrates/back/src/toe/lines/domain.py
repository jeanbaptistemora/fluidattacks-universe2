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
    ToeLinesState,
)
from newutils import (
    datetime as datetime_utils,
)
from newutils.validations import (
    validate_commit_hash_deco,
    validate_email_address_deco,
    validate_field_length_deco,
    validate_sanitized_csv_input_deco,
)
from roots import (
    domain as roots_domain,
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


def _get_optional_be_present_until(be_present: bool) -> datetime | None:
    return datetime_utils.get_utc_now() if be_present is False else None


def _assign_attacked_lines(
    *,
    filename: str,
    attributes: ToeLinesAttributesToAdd,
) -> int:
    if get_filename_extension(filename) in CHECKED_FILES:
        return attributes.loc
    if (
        attributes.attacked_at
        and attributes.last_commit_date
        and attributes.attacked_at <= attributes.last_commit_date
    ):
        return attributes.attacked_lines
    return 0


@validate_loc_deco("attributes.loc")
@validate_modified_date_deco("attributes.last_commit_date")
def _validate_assign_attacked_lines(
    *,
    filename: str,
    attributes: ToeLinesAttributesToAdd,
) -> int:
    return _assign_attacked_lines(filename=filename, attributes=attributes)


# pylint: disable=unused-argument
@validate_email_address_deco("seen_first_time_by")
def _validate_seen_first_time_by(
    *,
    seen_first_time_by: str,
) -> None:
    return


def _assign_toe_lines(
    *,
    attributes: ToeLinesAttributesToAdd,
    attacked_lines: int,
    filename: str,
    group_name: str,
    root: Root,
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
        filename=filename,
        group_name=group_name,
        root_id=root.id,
        seen_first_time_by=attributes.seen_first_time_by,
        state=ToeLinesState(
            attacked_at=attributes.attacked_at,
            attacked_by=attributes.attacked_by,
            attacked_lines=attacked_lines,
            be_present=attributes.be_present,
            be_present_until=be_present_until,
            comments=attributes.comments,
            first_attack_at=first_attack_at,
            has_vulnerabilities=has_vulnerabilities,
            modified_by=attributes.seen_first_time_by
            if attributes.seen_first_time_by
            else "machine@fluidattacks.com",
            modified_date=datetime_utils.get_utc_now(),
            last_author=attributes.last_author,
            last_commit=attributes.last_commit,
            last_commit_date=attributes.last_commit_date,
            loc=attributes.loc,
            seen_at=attributes.seen_at or datetime_utils.get_utc_now(),
            sorts_risk_level=attributes.sorts_risk_level,
        ),
    )


@validate_sanitized_csv_input_deco(["attributes.last_author", "filename"])
@validate_email_address_deco("attributes.last_author")
@validate_commit_hash_deco("attributes.last_commit")
@validate_git_root_deco("root")
@validate_active_root_deco("root")
def _validate_assign_toe_lines(
    *,
    attributes: ToeLinesAttributesToAdd,
    attacked_lines: int,
    filename: str,
    group_name: str,
    root: Root,
) -> ToeLines:
    return _assign_toe_lines(
        attributes=attributes,
        attacked_lines=attacked_lines,
        filename=filename,
        group_name=group_name,
        root=root,
    )


async def add(  # pylint: disable=too-many-arguments
    loaders: Dataloaders,
    group_name: str,
    root_id: str,
    filename: str,
    attributes: ToeLinesAttributesToAdd,
    is_moving_toe_lines: bool = False,
) -> None:
    root = await roots_domain.get_root(loaders, root_id, group_name)
    if is_moving_toe_lines is False:
        if attributes.seen_first_time_by is not None:
            _validate_seen_first_time_by(
                seen_first_time_by=attributes.seen_first_time_by
            )
        attacked_lines = _validate_assign_attacked_lines(
            filename=filename, attributes=attributes
        )
        toe_lines = _validate_assign_toe_lines(
            attributes=attributes,
            attacked_lines=attacked_lines,
            filename=filename,
            group_name=group_name,
            root=root,
        )
    else:
        attacked_lines = _assign_attacked_lines(
            filename=filename, attributes=attributes
        )
        toe_lines = _assign_toe_lines(
            attributes=attributes,
            attacked_lines=attacked_lines,
            filename=filename,
            group_name=group_name,
            root=root,
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


# pylint: disable=unused-argument
@validate_field_length_deco("comments", limit=200)
@validate_sanitized_csv_input_deco(["comments"])
def _validate_comments(*, comments: str) -> None:
    return


async def update(
    current_value: ToeLines,
    attributes: ToeLinesAttributesToUpdate,
    is_moving_toe_lines: bool = False,
) -> None:
    if (  # pylint: disable=too-many-boolean-expressions
        not is_moving_toe_lines
        and (
            attributes.attacked_at is not None
            and current_value.state.attacked_at is not None
        )
        and (
            attributes.attacked_at <= current_value.state.attacked_at
            or attributes.attacked_at > datetime_utils.get_utc_now()
            or attributes.attacked_at < current_value.state.seen_at
        )
    ):
        raise InvalidToeLinesAttackAt()

    loc = (
        attributes.loc
        if attributes.loc is not None
        else current_value.state.loc
    )
    if (
        is_moving_toe_lines is False
        and attributes.attacked_lines is not None
        and not (0 <= attributes.attacked_lines <= loc)
    ):
        raise InvalidToeLinesAttackedLines()

    if is_moving_toe_lines is False and attributes.comments is not None:
        _validate_comments(comments=attributes.comments)

    last_attacked_at = (
        attributes.attacked_at or current_value.state.attacked_at
    )
    last_commit_date = (
        attributes.last_commit_date or current_value.state.last_commit_date
    )
    first_attack_at = current_value.state.first_attack_at
    if attributes.first_attack_at is not None:
        first_attack_at = attributes.first_attack_at
    elif not current_value.state.first_attack_at and attributes.attacked_at:
        first_attack_at = attributes.attacked_at

    if get_filename_extension(current_value.filename) in CHECKED_FILES:
        attacked_lines = loc
    elif (
        attributes.attacked_lines != 0
        and last_attacked_at
        and last_commit_date <= last_attacked_at
    ):
        attacked_lines = min(
            attributes.attacked_lines or current_value.state.attacked_lines,
            loc,
        )
    else:
        attacked_lines = 0

    be_present_until = (
        current_value.state.be_present_until
        if attributes.be_present is None
        else _get_optional_be_present_until(attributes.be_present)
    )
    clean_be_present_until = (
        attributes.be_present is not None and be_present_until is None
    )
    current_be_present = (
        current_value.state.be_present
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
    new_state = ToeLinesState(
        attacked_at=attributes.attacked_at
        if attributes.attacked_at is not None
        else current_value.state.attacked_at,
        attacked_by=attributes.attacked_by
        if attributes.attacked_by is not None
        else current_value.state.attacked_by,
        attacked_lines=attacked_lines
        if attributes.attacked_lines is not None
        else current_value.state.attacked_lines,
        be_present=attributes.be_present
        if attributes.be_present is not None
        else current_value.state.be_present,
        be_present_until=be_present_until,
        comments=attributes.comments
        if attributes.comments is not None
        else current_value.state.comments,
        last_author=attributes.last_author
        if attributes.last_author is not None
        else current_value.state.last_author,
        first_attack_at=first_attack_at,
        has_vulnerabilities=has_vulnerabilities,
        loc=attributes.loc
        if attributes.loc is not None
        else current_value.state.loc,
        last_commit=attributes.last_commit
        if attributes.last_commit is not None
        else current_value.state.last_commit,
        last_commit_date=attributes.last_commit_date
        if attributes.last_commit_date is not None
        else current_value.state.last_commit_date,
        modified_by=attributes.attacked_by
        if attributes.attacked_by
        else "machine@fluidattacks.com",
        modified_date=datetime_utils.get_utc_now(),
        seen_at=attributes.seen_at
        if attributes.seen_at is not None
        else current_value.state.seen_at,
        sorts_risk_level=attributes.sorts_risk_level
        if attributes.sorts_risk_level is not None
        else current_value.state.sorts_risk_level,
        sorts_risk_level_date=attributes.sorts_risk_level_date
        if attributes.sorts_risk_level_date is not None
        else current_value.state.sorts_risk_level_date,
        sorts_suggestions=json.loads(json.dumps(attributes.sorts_suggestions))
        if attributes.sorts_suggestions is not None
        else current_value.state.sorts_suggestions,
    )
    if clean_be_present_until:
        new_state = new_state._replace(be_present_until=None)
    await toe_lines_model.update_state(
        current_value=current_value,
        new_state=new_state,
    )
