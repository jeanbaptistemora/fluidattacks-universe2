from aioextensions import (
    collect,
    in_thread,
)
import aiofiles  # type: ignore
import asyncio
from batch.types import (
    BatchProcessing,
)
from context import (
    FI_TOE_LINES_RULES,
)
from custom_exceptions import (
    ToeLinesAlreadyUpdated,
)
from dataloaders import (
    get_new_context,
)
from db_model.roots.types import (
    RootItem,
)
from db_model.toe_lines.types import (
    ToeLines,
)
from decimal import (
    Decimal,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from git.exc import (
    InvalidGitRepositoryError,
)
from git.repo.base import (
    Repo,
)
import logging
import logging.config
from newutils import (
    files as files_utils,
    git as git_utils,
)
import os
from roots import (
    domain as roots_domain,
)
from settings import (
    LOGGING,
)
import tempfile
from toe.lines import (
    domain as toe_lines_domain,
)
from toe.lines.types import (
    ToeLinesAttributesToAdd,
    ToeLinesAttributesToUpdate,
)
from typing import (
    cast,
    Dict,
    Set,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


CLOC_ENV = os.environ.copy()
CLOC_ENV["LC_ALL"] = "C"
CLOC_DOC_LANGS = ["Markdown"]
CLOC_STYLE_LANGS = ["CSS", "SASS", "LESS", "Stylus"]
CLOC_FORMAT_LANGS = ["XML", "XAML"]
CLOC_FORCE_LANG_DEF = "--force-lang-def=" + FI_TOE_LINES_RULES
CLOC_EXCLUDE_LIST = ",".join(
    CLOC_DOC_LANGS + CLOC_STYLE_LANGS + CLOC_FORMAT_LANGS
)
CLOC_EXCLUDE_LANG = "--exclude-lang=" + CLOC_EXCLUDE_LIST


toe_lines_add = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=10
)(toe_lines_domain.add)
toe_lines_update = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=10
)(toe_lines_domain.update)


async def apply_git_config(repo_path: str) -> None:
    """apply config in the git repository"""
    await asyncio.create_subprocess_exec(
        "git",
        f"--git-dir={repo_path}/.git",
        "config",
        "core.quotepath",
        "off",
    )


async def get_present_filenames(
    group_path: str, repo: Repo, repo_nickname: str
) -> Set[str]:
    trees = repo.head.commit.tree.traverse()
    ignored_files = await get_ignored_files(group_path, repo_nickname)
    included_head_filenames = tuple(
        tree.path
        for tree in trees
        if tree.type == "blob" and tree.path not in ignored_files
    )

    file_exists = await collect(
        in_thread(os.path.exists, f"{repo_nickname}/{filename}")
        for filename in included_head_filenames
    )

    file_islink = await collect(
        in_thread(os.path.islink, f"{repo_nickname}/{filename}")
        for filename in included_head_filenames
    )

    return {
        filename
        for filename, exists, islink in zip(
            included_head_filenames, file_exists, file_islink
        )
        if exists and not islink
    }


async def get_ignored_files(group_path: str, repo_nickname: str) -> Set[str]:
    ignored_filename = f"{group_path}/{repo_nickname}_ignored.txt"
    ignored_files = set()
    call_cloc = (
        "cloc",
        CLOC_FORCE_LANG_DEF,
        CLOC_EXCLUDE_LANG,
        repo_nickname,
        "--ignored",
        ignored_filename,
        "--timeout",
        "900",
    )
    await asyncio.create_subprocess_exec(
        *call_cloc,
        env=CLOC_ENV,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.STDOUT,
    )
    repo_nickname_len = len(repo_nickname) + 1
    async with aiofiles.open(
        ignored_filename, "r", encoding="utf8"
    ) as outfile:
        lines = await outfile.readlines()
        ignored_files = {
            line.split(":  ")[0][repo_nickname_len:] for line in lines
        }

    return ignored_files


async def get_present_toe_lines_to_add(
    present_filenames: Set[str],
    repo: Repo,
    repo_nickname: str,
    repo_toe_lines: Dict[str, ToeLines],
) -> Tuple[Tuple[str, ToeLinesAttributesToAdd], ...]:
    non_db_filenames = tuple(
        filename
        for filename in present_filenames
        if not repo_toe_lines.get(filename)
    )
    last_locs = await collect(
        tuple(
            files_utils.get_lines_count(f"{repo_nickname}/{filename}")
            for filename in non_db_filenames
        )
    )
    last_modified_commits = await collect(
        tuple(
            git_utils.get_last_commit_hash(repo, filename)
            for filename in non_db_filenames
        )
    )
    last_modified_dates = await collect(
        tuple(
            git_utils.get_last_modified_date(repo, filename)
            for filename in non_db_filenames
        )
    )
    last_commit_authors = await collect(
        tuple(
            git_utils.get_last_commit_author(repo, filename)
            for filename in non_db_filenames
        )
    )
    return tuple(
        (
            filename,
            ToeLinesAttributesToAdd(
                attacked_at="",
                attacked_by="",
                attacked_lines=0,
                be_present=True,
                commit_author=last_commit_author,
                comments="",
                first_attack_at="",
                loc=last_loc,
                modified_commit=last_modified_commit,
                modified_date=last_modified_date,
                sorts_risk_level=Decimal("-1"),
            ),
        )
        for (
            filename,
            last_commit_author,
            last_loc,
            last_modified_commit,
            last_modified_date,
        ) in zip(
            non_db_filenames,
            last_commit_authors,
            last_locs,
            last_modified_commits,
            last_modified_dates,
        )
    )


async def get_present_toe_lines_to_update(
    present_filenames: Set[str],
    repo: Repo,
    repo_nickname: str,
    repo_toe_lines: Dict[str, ToeLines],
) -> Tuple[Tuple[ToeLines, ToeLinesAttributesToUpdate], ...]:
    db_filenames = tuple(
        filename
        for filename in present_filenames
        if repo_toe_lines.get(filename)
    )
    last_locs = await collect(
        tuple(
            files_utils.get_lines_count(f"{repo_nickname}/{filename}")
            for filename in db_filenames
        )
    )
    last_modified_commits = await collect(
        tuple(
            git_utils.get_last_commit_hash(repo, filename)
            for filename in db_filenames
        )
    )
    last_modified_dates = await collect(
        tuple(
            git_utils.get_last_modified_date(repo, filename)
            for filename in db_filenames
        )
    )
    last_commit_authors = await collect(
        tuple(
            git_utils.get_last_commit_author(repo, filename)
            for filename in db_filenames
        )
    )
    be_present = True
    return tuple(
        (
            repo_toe_lines[filename],
            ToeLinesAttributesToUpdate(
                be_present=be_present,
                commit_author=last_commit_author,
                loc=last_loc,
                modified_commit=last_modified_commit,
                modified_date=last_modified_date,
            ),
        )
        for (
            filename,
            last_commit_author,
            last_loc,
            last_modified_commit,
            last_modified_date,
        ) in zip(
            db_filenames,
            last_commit_authors,
            last_locs,
            last_modified_commits,
            last_modified_dates,
        )
        if (
            be_present,
            last_commit_author,
            last_loc,
            last_modified_commit,
            last_modified_date,
        )
        != (
            repo_toe_lines[filename].be_present,
            repo_toe_lines[filename].commit_author,
            repo_toe_lines[filename].loc,
            repo_toe_lines[filename].modified_commit,
            repo_toe_lines[filename].modified_date,
        )
    )


def get_non_present_toe_lines_to_update(
    present_filenames: Set[str],
    repo_toe_lines: Dict[str, ToeLines],
) -> Tuple[Tuple[ToeLines, ToeLinesAttributesToUpdate], ...]:
    return tuple(
        (
            repo_toe_lines[db_filename],
            ToeLinesAttributesToUpdate(
                be_present=False,
            ),
        )
        for db_filename in repo_toe_lines
        if db_filename not in present_filenames
        and repo_toe_lines[db_filename].be_present
    )


def make_group_dir(tmpdir: str, group_name: str) -> None:
    group_dir = os.path.join(tmpdir, "groups", group_name)
    os.makedirs(group_dir, exist_ok=True)


def pull_repositories(tmpdir: str, group_name: str) -> None:
    make_group_dir(tmpdir, group_name)
    os.system(  # nosec
        "CI=true "
        "CI_COMMIT_REF_NAME=master "
        "PROD_AWS_ACCESS_KEY_ID=$SERVICES_PROD_AWS_ACCESS_KEY_ID "
        "PROD_AWS_SECRET_ACCESS_KEY=$SERVICES_PROD_AWS_SECRET_ACCESS_KEY "
        f"melts drills --pull-repos {group_name} "
    )


@retry_on_exceptions(
    exceptions=(ToeLinesAlreadyUpdated,),
)
async def refresh_repo_toe_lines(
    group_name: str, group_path: str, repo_nickname: str
) -> None:
    try:
        repo = Repo(repo_nickname)
    except InvalidGitRepositoryError:
        LOGGER.error(
            "Invalid repository",
            extra={
                "extra": {
                    "group_name": group_name,
                    "repository": repo_nickname,
                }
            },
        )
        return

    loaders = get_new_context()
    await apply_git_config(repo_nickname)
    roots: Tuple[RootItem, ...] = await loaders.group_roots.load(group_name)
    root_id = roots_domain.get_root_id_by_nickname(repo_nickname, roots)
    repo_toe_lines = {
        toe_lines.filename: toe_lines
        for toe_lines in cast(
            Tuple[ToeLines, ...],
            await loaders.root_toe_lines.load((group_name, root_id)),
        )
    }
    present_filenames = await get_present_filenames(
        group_path, repo, repo_nickname
    )
    present_toe_lines_to_add = await get_present_toe_lines_to_add(
        present_filenames,
        repo,
        repo_nickname,
        repo_toe_lines,
    )
    await collect(
        tuple(
            toe_lines_add(group_name, root_id, filename, toe_lines_to_add)
            for filename, toe_lines_to_add in present_toe_lines_to_add
        ),
        workers=500,
    )
    present_toe_lines_to_update = await get_present_toe_lines_to_update(
        present_filenames,
        repo,
        repo_nickname,
        repo_toe_lines,
    )
    non_present_toe_lines_to_update = get_non_present_toe_lines_to_update(
        present_filenames,
        repo_toe_lines,
    )
    await collect(
        tuple(
            toe_lines_update(current_value, attrs_to_update)
            for current_value, attrs_to_update in present_toe_lines_to_update
            + non_present_toe_lines_to_update
        ),
        workers=500,
    )


async def refresh_toe_lines(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    current_dir = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        pull_repositories(tmpdir, group_name)
        group_path = tmpdir + f"/groups/{group_name}"
        os.chdir(f"{group_path}/fusion")
        fusion_files = os.listdir()
        is_dir = await collect(
            tuple(in_thread(os.path.isdir, file) for file in fusion_files)
        )
        await collect(
            tuple(
                refresh_repo_toe_lines(group_name, group_path, fusion_file)
                for fusion_file, is_dir in zip(fusion_files, is_dir)
                if is_dir
            )
        )
        os.chdir(current_dir)
