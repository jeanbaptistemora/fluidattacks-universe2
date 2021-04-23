# Standard libraries
import csv
import glob
import logging
import logging.config
import re
import tempfile
from typing import (
    Any,
    Callable,
    List,
    Set,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
    in_process,
)

# Local libraries
from back.settings import (
    LOGGING,
)
from backend.api import get_new_context
from custom_exceptions import (
    GroupNameNotFound,
    RootNotFound,
)
from data_containers.toe_lines import GitRootToeLines
from newutils import (
    bugsnag as bugsnag_utils,
    datetime as datetime_utils,
    git as git_utils,
)
from roots import domain as roots_domain
from roots.types import Root
from toe.lines import domain as toe_lines_domain


# Constants
DEFAULT_FILENAMES = (
    'Repo1/Folder1/Folder2/File.js',
    'Repo1/Folder1/Folder2/Folder3/File.html',
    'Repo2/Folder1/File.cs',
)
logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)

bugsnag_utils.start_scheduler_session()


def _format_date(date_str: str) -> str:
    date = datetime_utils.get_from_str(date_str, date_format='%Y-%m-%d')
    formated_date_str = date.isoformat()

    return formated_date_str


def _format_filename(filename: str) -> str:
    return filename.strip('"')


def _get_group_toe_lines_from_cvs(
    lines_csv_path: str,
    group_name: str,
    group_roots: Tuple[Root, ...]
) -> Set[GitRootToeLines]:
    default_date = datetime_utils.DEFAULT_ISO_STR
    lines_csv_fields: List[Tuple[str, Callable, Any, str]] = [
        # field_name, field_formater, field_default_value, cvs_field_name,
        ('filename', _format_filename, '', 'filename'),
        ('comments', str, '', 'comments'),
        ('modified_commit', str, '', 'modified-commit'),
        ('loc', int, 0, 'loc'),
        ('tested_lines', int, 0, 'tested-lines'),
        ('modified_date', _format_date, default_date, 'modified-date'),
        ('tested_date', _format_date, default_date, 'tested-date'),
    ]
    group_toe_lines = set()
    with open(lines_csv_path) as csv_file:
        for row in csv.DictReader(csv_file):
            new_toe_lines = dict()
            for (
                field_name,
                formater,
                default_value,
                cvs_field_name
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

            if new_toe_lines['filename'] in DEFAULT_FILENAMES:
                continue
            try:
                new_toe_lines['root_id'] = (
                    roots_domain.get_root_id_by_filename(
                        new_toe_lines['filename'],
                        group_roots
                    )
                )
            except RootNotFound as ex:
                LOGGER.exception(ex, extra={'extra': locals()})
                raise ex

            new_toe_lines['group_name'] = group_name
            new_toe_lines['sorts_risk_level'] = 0
            group_toe_lines.add(GitRootToeLines(**new_toe_lines))

    return group_toe_lines


def _get_toe_lines_to_add(
    group_toe_lines: Set[GitRootToeLines],
    group_toe_lines_hashes: Set[int],
    cvs_group_toe_lines: Set[GitRootToeLines]
) -> Set[GitRootToeLines]:
    return {
        toe_lines
        for toe_lines in cvs_group_toe_lines
        if toe_lines not in group_toe_lines
        and toe_lines.get_hash() not in group_toe_lines_hashes
    }


def _get_toe_lines_to_update(
    group_toe_lines: Set[GitRootToeLines],
    group_toe_lines_hashes: Set[int],
    cvs_group_toe_lines: Set[GitRootToeLines]
) -> Set[GitRootToeLines]:
    return {
        toe_lines
        for toe_lines in cvs_group_toe_lines
        if toe_lines not in group_toe_lines
        and toe_lines.get_hash() in group_toe_lines_hashes
    }


def _get_toe_lines_to_remove(
    group_toe_lines: Set[GitRootToeLines],
    cvs_group_toe_lines_hashes: Set[int]
) -> Set[GitRootToeLines]:
    return {
        toe_lines
        for toe_lines in group_toe_lines
        if toe_lines.get_hash() not in cvs_group_toe_lines_hashes
    }


async def update_toe_lines_from_csv(
    loaders: Any,
    group_name: str,
    lines_csv_path: str
) -> None:
    group_roots_loader = loaders.group_roots
    group_roots: Tuple[Root, ...] = await group_roots_loader.load(group_name)
    group_toe_lines_loader = loaders.group_toe_lines
    group_toe_lines: Set[GitRootToeLines] = set(
        await group_toe_lines_loader.load(group_name)
    )
    group_toe_lines_hashes = {
        toe_lines.get_hash()
        for toe_lines in group_toe_lines
    }
    cvs_group_toe_lines = await in_process(
        _get_group_toe_lines_from_cvs,
        lines_csv_path,
        group_name,
        group_roots
    )
    cvs_group_toe_lines_hashes = {
        toe_lines.get_hash()
        for toe_lines in cvs_group_toe_lines
    }
    toe_lines_to_update = await in_process(
        _get_toe_lines_to_update,
        group_toe_lines,
        group_toe_lines_hashes,
        cvs_group_toe_lines
    )
    await collect([
        toe_lines_domain.update(toe_lines)
        for toe_lines in toe_lines_to_update
    ])
    toe_lines_to_remove = await in_process(
        _get_toe_lines_to_remove,
        group_toe_lines,
        cvs_group_toe_lines_hashes
    )
    await collect([
        toe_lines_domain.delete(
            toe_lines.filename,
            toe_lines.group_name,
            toe_lines.root_id
        )
        for toe_lines in toe_lines_to_remove
    ])
    toe_lines_to_add = await in_process(
        _get_toe_lines_to_add,
        group_toe_lines,
        group_toe_lines_hashes,
        cvs_group_toe_lines
    )
    await collect([
        toe_lines_domain.add(toe_lines)
        for toe_lines in toe_lines_to_add
    ])


def _get_group_name(
    tmpdirname: str,
    lines_csv_path: str
) -> str:
    group_match = re.match(
        pattern=fr'{tmpdirname}/groups/(\w+)',
        string=lines_csv_path
    )
    if not group_match:
        raise GroupNameNotFound()

    return group_match.groups('1')[0]


async def main() -> None:
    """Update the root toe lines from services repository"""
    loaders = get_new_context()
    with tempfile.TemporaryDirectory() as tmpdirname:
        git_utils.clone_services_repository(tmpdirname)
        lines_csv_glob = f'{tmpdirname}/groups/*/toe/lines.csv'
        lines_cvs_paths = glob.glob(lines_csv_glob)
        lines_csv_group_names = [
            _get_group_name(tmpdirname, lines_cvs_path)
            for lines_cvs_path in lines_cvs_paths
        ]
        await collect([
            update_toe_lines_from_csv(
                loaders,
                group_name,
                lines_csv_path
            )
            for lines_csv_path, group_name
            in zip(lines_cvs_paths, lines_csv_group_names)
        ])
