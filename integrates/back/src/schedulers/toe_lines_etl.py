from aioextensions import (
    collect,
)
import csv
from custom_exceptions import (
    GroupNameNotFound,
    RootNotFound,
    UnavailabilityError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from decorators import (
    retry_on_exceptions,
)
import glob
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils import (
    bugsnag as bugsnag_utils,
    datetime as datetime_utils,
    git as git_utils,
    utils,
)
import os
import re
from roots import (
    domain as roots_domain,
)
from roots.types import (
    Root,
)
from settings import (
    LOGGING,
)
import tempfile
from toe.lines import (
    domain as toe_lines_domain,
)
from typing import (
    Any,
    Callable,
    List,
    Set,
    Tuple,
)
from urllib.parse import (
    unquote,
)

# Constants
INVALID_FILENAMES = {
    "",
    "Repo1/Folder1/Folder2/File.js",
    "Repo1/Folder1/Folder2/Folder3/File.html",
    "Repo2/Folder1/File.cs",
}
IGNORED_SERVICES_REPO_GROUP = {"kadugli", "wareham"}
logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

bugsnag_utils.start_scheduler_session()

toe_lines_add = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=10
)(toe_lines_domain.add)
toe_lines_remove = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=10
)(toe_lines_domain.remove)
toe_lines_update = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=10
)(toe_lines_domain.update)


def _format_date(date_str: str) -> str:
    date = datetime_utils.get_from_str(date_str, date_format="%Y-%m-%d")
    formatted_date_str = date.isoformat()

    return formatted_date_str


def _format_filename(filename: str) -> str:
    nickname, path = filename.strip('"').split("/", 1)
    formatted_nickname = re.sub(
        r"(?![a-zA-Z_0-9-]).",
        "_",
        unquote(nickname).rstrip()[:128],
    )

    return "/".join([formatted_nickname, path])


def _get_group_toe_lines_from_cvs(
    lines_csv_path: str, group_name: str, group_roots: Tuple[Root, ...]
) -> Set[ToeLines]:
    default_date = datetime_utils.DEFAULT_ISO_STR
    lines_csv_fields: List[Tuple[str, Callable, Any, str]] = [
        # field_name, field_formater, field_default_value, cvs_field_name,
        ("filename", _format_filename, "", "filename"),
        ("comments", str, "", "comments"),
        ("modified_commit", str, "", "modified-commit"),
        ("loc", int, 0, "loc"),
        ("tested_lines", int, 0, "tested-lines"),
        ("modified_date", _format_date, default_date, "modified-date"),
        ("tested_date", _format_date, default_date, "tested-date"),
    ]
    group_toe_lines = set()
    with open(  # pylint: disable=unspecified-encoding
        lines_csv_path
    ) as csv_file:
        for row in csv.DictReader(csv_file):
            new_toe_lines = {}
            for (
                field_name,
                formater,
                default_value,
                cvs_field_name,
            ) in lines_csv_fields:
                cvs_field_value = row.get(cvs_field_name)
                try:
                    new_toe_lines[field_name] = (
                        formater(cvs_field_value)
                        if cvs_field_value
                        else default_value
                    )
                except ValueError:
                    new_toe_lines[field_name] = default_value

            if new_toe_lines["filename"] in INVALID_FILENAMES:
                continue
            try:
                new_toe_lines[
                    "root_id"
                ] = roots_domain.get_root_id_by_filename(
                    new_toe_lines["filename"], group_roots
                )
            except RootNotFound as ex:
                LOGGER.exception(ex, extra={"extra": locals()})
                raise ex

            new_toe_lines["group_name"] = group_name
            new_toe_lines["sorts_risk_level"] = 0
            group_toe_lines.add(ToeLines(**new_toe_lines))

    return group_toe_lines


def _get_toe_lines_to_add(
    group_toe_lines: Set[ToeLines],
    group_toe_lines_hashes: Set[int],
    cvs_group_toe_lines: Set[ToeLines],
) -> Set[ToeLines]:
    return {
        toe_lines
        for toe_lines in cvs_group_toe_lines
        if toe_lines not in group_toe_lines
        and toe_lines.get_hash() not in group_toe_lines_hashes
    }


def _get_toe_lines_to_update(
    group_toe_lines: Set[ToeLines],
    group_toe_lines_hashes: Set[int],
    cvs_group_toe_lines: Set[ToeLines],
) -> Set[ToeLines]:
    # Exclude sortsRiskLevel from updating, its value must remain
    cvs_group_toe_lines_copy = cvs_group_toe_lines.copy()
    for toe_lines_csv in cvs_group_toe_lines_copy:
        group_toes = [
            toe_lines
            for toe_lines in group_toe_lines
            if toe_lines.get_hash() == toe_lines_csv.get_hash()
        ]
        for toe_lines in group_toes:
            cvs_group_toe_lines.discard(toe_lines_csv)
            toe_lines_csv = toe_lines_csv._replace(
                sorts_risk_level=toe_lines.sorts_risk_level
            )
            cvs_group_toe_lines.add(toe_lines_csv)

    return {
        toe_lines
        for toe_lines in cvs_group_toe_lines
        if toe_lines not in group_toe_lines
        and toe_lines.get_hash() in group_toe_lines_hashes
    }


def _get_toe_lines_to_remove(
    group_toe_lines: Set[ToeLines], cvs_group_toe_lines_hashes: Set[int]
) -> Set[ToeLines]:
    return {
        toe_lines
        for toe_lines in group_toe_lines
        if toe_lines.get_hash() not in cvs_group_toe_lines_hashes
    }


async def update_toe_lines_from_csv(
    loaders: Any, group_name: str, lines_csv_path: str
) -> None:
    LOGGER_CONSOLE.info(
        "Updating toe lines", extra={"extra": {"group_name": group_name}}
    )
    group_roots_loader = loaders.group_roots
    group_roots: Tuple[Root, ...] = await group_roots_loader.load(group_name)
    group_toe_lines_loader = loaders.group_toe_lines
    group_toe_lines: Set[ToeLines] = set(
        await group_toe_lines_loader.load(group_name)
    )
    group_toe_lines_hashes = {
        toe_lines.get_hash() for toe_lines in group_toe_lines
    }
    cvs_group_toe_lines = _get_group_toe_lines_from_cvs(
        lines_csv_path, group_name, group_roots
    )
    cvs_group_toe_lines_hashes = {
        toe_lines.get_hash() for toe_lines in cvs_group_toe_lines
    }
    toe_lines_to_update = _get_toe_lines_to_update(
        group_toe_lines,
        group_toe_lines_hashes,
        cvs_group_toe_lines,
    )
    await collect(
        [toe_lines_update(toe_lines) for toe_lines in toe_lines_to_update],
        workers=100,
    )
    toe_lines_to_remove = _get_toe_lines_to_remove(
        group_toe_lines, cvs_group_toe_lines_hashes
    )
    await collect(
        [
            toe_lines_remove(
                toe_lines.filename, toe_lines.group_name, toe_lines.root_id
            )
            for toe_lines in toe_lines_to_remove
        ],
        workers=100,
    )
    toe_lines_to_add = _get_toe_lines_to_add(
        group_toe_lines,
        group_toe_lines_hashes,
        cvs_group_toe_lines,
    )
    await collect(
        [toe_lines_add(toe_lines) for toe_lines in toe_lines_to_add],
        workers=100,
    )


def _get_group_name(tmpdirname: str, lines_csv_path: str) -> str:
    group_match = re.match(
        pattern=fr"{tmpdirname}/groups/(\w+)", string=lines_csv_path
    )
    if not group_match:
        raise GroupNameNotFound()

    return group_match.groups("1")[0]


async def update_toe_lines(loaders: Dataloaders, tmpdirname: str) -> None:
    lines_csv_glob = f"{tmpdirname}/groups/*/toe/lines.csv"
    lines_cvs_paths = glob.glob(lines_csv_glob)
    lines_csv_group_names = [
        _get_group_name(tmpdirname, lines_cvs_path)
        for lines_cvs_path in lines_cvs_paths
    ]
    await collect(
        [
            update_toe_lines_from_csv(loaders, group_name, lines_csv_path)
            for lines_csv_path, group_name in zip(
                lines_cvs_paths, lines_csv_group_names
            )
        ],
        workers=10,
    )


async def _get_machine_only_groups() -> List[str]:
    LOGGER_CONSOLE.info("Getting machine only groups", extra={"extra": {}})
    active_groups = await groups_domain.get_active_groups()
    groups_data = await collect(
        groups_domain.get_attributes(group, ["historic_configuration"])
        for group in active_groups
    )
    groups_config = [
        data["historic_configuration"][-1] for data in groups_data
    ]
    return [
        group
        for group, config in zip(active_groups, groups_config)
        if (
            utils.get_key_or_fallback(
                config, "has_machine", "has_skims", False
            )
            and not utils.get_key_or_fallback(
                config, "has_squad", "has_drills", False
            )
        )
    ]


def _create_group_basic_structure(tmpdirname: str, group: str) -> None:
    toe_dir = os.path.join(tmpdirname, "groups", group, "toe")
    os.makedirs(toe_dir, exist_ok=True)
    with open(  # pylint: disable=unspecified-encoding
        os.path.join(toe_dir, "lines.csv"), mode="w"
    ) as toe:
        columns = [
            "filename",
            "loc",
            "tested-lines",
            "modified-date",
            "modified-commit",
            "tested-date",
            "comments",
        ]
        writer = csv.DictWriter(toe, columns)
        writer.writeheader()


async def update_toe_lines_machine_groups(loaders: Dataloaders) -> None:
    groups = await _get_machine_only_groups()
    current_dir = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname)
        os.environ["PROD_AWS_ACCESS_KEY_ID"] = os.environ.get(
            "SERVICES_PROD_AWS_ACCESS_KEY_ID", ""
        )
        os.environ["PROD_AWS_SECRET_ACCESS_KEY"] = os.environ.get(
            "SERVICES_PROD_AWS_SECRET_ACCESS_KEY", ""
        )
        for group in groups:
            _create_group_basic_structure(tmpdirname, group)
            os.system(  # nosec
                f"melts drills --pull-repos {group} && "
                f"melts drills --update-lines {group}"
            )
        await update_toe_lines(loaders, tmpdirname)
    os.chdir(current_dir)


async def main() -> None:
    """Update the root toe lines from services repository"""
    loaders = get_new_context()
    with tempfile.TemporaryDirectory() as tmpdirname:
        git_utils.clone_services_repository(tmpdirname)
        for group in IGNORED_SERVICES_REPO_GROUP:
            lines_path = f"{tmpdirname}/groups/{group}/toe/lines.csv"
            if os.path.exists(lines_path):
                os.remove(lines_path)
        await update_toe_lines(loaders, tmpdirname)
    await update_toe_lines_machine_groups(loaders)
