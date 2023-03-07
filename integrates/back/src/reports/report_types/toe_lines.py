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

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


def _get_valid_field(field: str) -> str:
    with suppress(UnsanitizedInputFound):
        validate_sanitized_csv_input(field)
        return field
    return ""


async def get_group_toe_lines_report(
    *,
    loaders: Dataloaders,
    group_name: str,
) -> str:
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

    group_toe_lines: list[ToeLines] = [
        edge.node
        for connection in roots_toe_lines
        for edge in connection.edges
    ]

    for toe_line in group_toe_lines:
        rows.append(
            [
                str(toe_line.state.be_present),
                _get_valid_field(toe_line.filename),
                str(toe_line.state.has_vulnerabilities),
                _get_valid_field(toe_line.state.last_author),
                _get_valid_field(toe_line.state.last_commit),
                str(toe_line.state.loc),
                toe_line.root_id,
                _get_valid_field(
                    root_nickname_by_id[toe_line.root_id.lower()]
                ),
                str(toe_line.state.last_commit_date),
            ]
        )

    date: str = get_as_str(get_now(), date_format="%Y-%m-%dT%H-%M-%S")
    csv_filename = f"{group_name}-{date}.csv"

    with tempfile.NamedTemporaryFile() as temp_file:
        target = temp_file.name + f"_{csv_filename}"

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
