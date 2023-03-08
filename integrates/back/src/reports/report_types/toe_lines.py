from authz import (
    get_group_level_enforcer,
)
from collections import (
    defaultdict,
)
from contextlib import (
    suppress,
)
import csv
from custom_exceptions import (
    UnsanitizedInputFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRoot,
    Root,
)
from db_model.toe_lines.types import (
    RootToeLinesRequest,
    ToeLines,
)
from decimal import (
    Decimal,
)
import logging
import logging.config
from newutils.datetime import (
    get_as_str,
    get_now,
)
from newutils.validations import (
    validate_sanitized_csv_input,
)
import os
from settings.logger import (
    LOGGING,
)
import tempfile
from typing import (
    NamedTuple,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


class SpecialFields(NamedTuple):
    attacked_at: bool
    attacked_by: bool
    attacked_lines: bool
    be_present_until: bool
    comments: bool
    first_attack_at: bool
    coverage: bool


def _get_valid_field(field: str) -> str:
    with suppress(UnsanitizedInputFound):
        validate_sanitized_csv_input(field)
        return field
    return ""


def _get_coverage(*, toe_line: ToeLines) -> str:
    return str(
        1
        if toe_line.state.loc == 0
        else Decimal(
            toe_line.state.attacked_lines / toe_line.state.loc
        ).quantize(Decimal("0.001"))
    )


def _get_row(
    *,
    toe_line: ToeLines,
    root_nickname_by_id: defaultdict[str, str],
    special_fields: SpecialFields,
) -> list[str]:
    return [
        str(toe_line.state.be_present),
        _get_valid_field(toe_line.filename),
        str(toe_line.state.has_vulnerabilities),
        _get_valid_field(toe_line.state.last_author),
        _get_valid_field(toe_line.state.last_commit),
        str(toe_line.state.loc),
        toe_line.root_id,
        _get_valid_field(root_nickname_by_id[toe_line.root_id.lower()]),
        str(toe_line.state.last_commit_date),
        *(
            [str(toe_line.state.attacked_at)]
            if special_fields.attacked_at
            else []
        ),
        *(
            [_get_valid_field(toe_line.state.attacked_by)]
            if special_fields.attacked_by
            else []
        ),
        *(
            [str(toe_line.state.attacked_lines)]
            if special_fields.attacked_lines
            else []
        ),
        *(
            [str(toe_line.state.be_present_until)]
            if special_fields.be_present_until
            else []
        ),
        *(
            [_get_valid_field(toe_line.state.comments)]
            if special_fields.comments
            else []
        ),
        *(
            [str(toe_line.state.first_attack_at)]
            if special_fields.first_attack_at
            else []
        ),
        *(
            [_get_coverage(toe_line=toe_line)]
            if special_fields.coverage
            else []
        ),
    ]


async def get_group_toe_lines_report(
    *,
    loaders: Dataloaders,
    group_name: str,
    email: str,
) -> str:
    enforcer = await get_group_level_enforcer(loaders, email)
    special_fields = SpecialFields(
        attacked_at=enforcer(
            group_name, "api_resolvers_toe_lines_attacked_at_resolve"
        ),
        attacked_by=enforcer(
            group_name, "api_resolvers_toe_lines_attacked_by_resolve"
        ),
        attacked_lines=enforcer(
            group_name, "api_resolvers_toe_lines_attacked_lines_resolve"
        ),
        be_present_until=enforcer(
            group_name, "api_resolvers_toe_lines_be_present_until_resolve"
        ),
        comments=enforcer(
            group_name, "api_resolvers_toe_lines_comments_resolve"
        ),
        first_attack_at=enforcer(
            group_name, "api_resolvers_toe_lines_first_attack_at_resolve"
        ),
        coverage=enforcer(group_name, "see_toe_lines_coverage"),
    )
    rows: list[list[str]] = [
        [
            "bePresent",
            "filename",
            "hasVulnerabilities",
            "lastAuthor",
            "lastCommit",
            "loc",
            "rootId",
            "rootNickname",
            "modifiedDate",
            *(["attackedAt"] if special_fields.attacked_at else []),
            *(["attackedBy"] if special_fields.attacked_by else []),
            *(["attackedLines"] if special_fields.attacked_lines else []),
            *(["bePresentUntil"] if special_fields.be_present_until else []),
            *(["comments"] if special_fields.comments else []),
            *(["firstAttackAt"] if special_fields.first_attack_at else []),
            *(["coverage"] if special_fields.coverage else []),
        ]
    ]
    group_roots: list[Root] = await loaders.group_roots.load(group_name)
    root_nickname_by_id: defaultdict[str, str] = defaultdict(str)

    for root in group_roots:
        root_nickname_by_id[root.id.lower()] = root.state.nickname

    roots_toe_lines = await loaders.root_toe_lines.load_many(
        [
            RootToeLinesRequest(group_name=group_name, root_id=root.id)
            for root in group_roots
            if isinstance(root, GitRoot)
        ]
    )

    for toe_line in [
        edge.node
        for connection in roots_toe_lines
        for edge in connection.edges
    ]:
        rows.append(
            _get_row(
                toe_line=toe_line,
                root_nickname_by_id=root_nickname_by_id,
                special_fields=special_fields,
            )
        )

    with tempfile.NamedTemporaryFile() as temp_file:
        target = (
            temp_file.name
            + f"_{group_name}-"
            + f'{get_as_str(get_now(), date_format="%Y-%m-%dT%H-%M-%S")}.csv'
        )

    with open(
        os.path.join(target),
        mode="w",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.writer(
            csv_file,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writerow(rows[0])
        writer.writerows(rows[1:])

    return csv_file.name
