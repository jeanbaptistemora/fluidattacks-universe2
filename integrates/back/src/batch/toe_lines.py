from aioextensions import (
    collect,
    in_thread,
)
import aiofiles  # type: ignore
import asyncio
from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
from context import (
    FI_TOE_LINES_RULES,
)
from custom_exceptions import (
    RepeatedToeLines,
    ToeLinesAlreadyUpdated,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.roots.types import (
    GitRootItem,
    RootItem,
)
from db_model.toe_lines.types import (
    RootToeLinesRequest,
    ToeLines,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from git.exc import (
    GitCommandError,
    InvalidGitRepositoryError,
    NoSuchPathError,
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
from settings import (
    LOGGING,
)
from subprocess import (  # nosec
    SubprocessError,
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
    Dict,
    Optional,
    Set,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


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
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_lines_domain.add)
toe_lines_update = retry_on_exceptions(
    exceptions=(UnavailabilityError,), sleep_seconds=5
)(toe_lines_domain.update)
files_get_lines_count = retry_on_exceptions(
    exceptions=(FileNotFoundError, OSError),
    max_attempts=10,
)(files_utils.get_lines_count)
git_get_last_commit_info = retry_on_exceptions(
    exceptions=(
        FileNotFoundError,
        GitCommandError,
        IndexError,
        OSError,
        SubprocessError,
        ValueError,
    )
)(git_utils.get_last_commit_info)


async def get_present_filenames(
    group_path: str, repo: Repo, repo_nickname: str
) -> Set[str]:
    LOGGER_CONSOLE.info(
        "Getting present filenames",
        extra={
            "extra": {
                "repo_nickname": repo_nickname,
            }
        },
    )
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
    LOGGER_CONSOLE.info(
        "Getting ignored files",
        extra={
            "extra": {
                "repo_nickname": repo_nickname,
            }
        },
    )
    ignored_filename = f"{group_path}/{repo_nickname}_ignored.txt"
    ignored_files = set()
    call_cloc = (
        "cloc",
        CLOC_FORCE_LANG_DEF,
        CLOC_EXCLUDE_LANG,
        repo_nickname,
        "--ignored",
        ignored_filename,
        "--diff-timeout",
        "900",
    )
    process = await asyncio.create_subprocess_exec(
        *call_cloc,
        env=CLOC_ENV,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.STDOUT,
    )
    await process.wait()
    repo_nickname_len = len(repo_nickname) + 1
    if await in_thread(os.path.exists, ignored_filename):
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
    LOGGER_CONSOLE.info(
        "Getting present toe lines to add",
        extra={
            "extra": {
                "repo_nickname": repo_nickname,
            }
        },
    )
    non_db_filenames = tuple(
        filename
        for filename in present_filenames
        if not repo_toe_lines.get(filename)
    )
    last_locs = await collect(
        tuple(
            files_get_lines_count(f"{repo_nickname}/{filename}")
            for filename in non_db_filenames
        ),
        workers=340,
    )
    last_commit_infos = await collect(
        tuple(
            git_get_last_commit_info(repo, filename)
            for filename in non_db_filenames
        ),
    )
    return tuple(
        (
            filename,
            ToeLinesAttributesToAdd(
                attacked_at="",
                attacked_by="",
                attacked_lines=0,
                commit_author=last_commit_info.author,
                comments="",
                loc=last_loc,
                modified_commit=last_commit_info.hash,
                modified_date=last_commit_info.modified_date,
                sorts_risk_level=-1,
            ),
        )
        for (filename, last_commit_info, last_loc,) in zip(
            non_db_filenames,
            last_commit_infos,
            last_locs,
        )
    )


async def get_present_toe_lines_to_update(
    present_filenames: Set[str],
    repo: Repo,
    repo_nickname: str,
    repo_toe_lines: Dict[str, ToeLines],
) -> Tuple[Tuple[ToeLines, ToeLinesAttributesToUpdate], ...]:
    LOGGER_CONSOLE.info(
        "Getting present toe lines to update",
        extra={
            "extra": {
                "repo_nickname": repo_nickname,
            }
        },
    )
    db_filenames = tuple(
        filename
        for filename in present_filenames
        if repo_toe_lines.get(filename)
    )
    last_locs = await collect(
        tuple(
            files_get_lines_count(f"{repo_nickname}/{filename}")
            for filename in db_filenames
        ),
        workers=340,
    )
    last_commit_infos = await collect(
        tuple(
            git_get_last_commit_info(repo, filename)
            for filename in db_filenames
        ),
    )
    be_present = True
    return tuple(
        (
            repo_toe_lines[filename],
            ToeLinesAttributesToUpdate(
                be_present=be_present,
                commit_author=last_commit_info.author,
                loc=last_loc,
                modified_commit=last_commit_info.hash,
                modified_date=last_commit_info.modified_date,
            ),
        )
        for (filename, last_commit_info, last_loc,) in zip(
            db_filenames,
            last_commit_infos,
            last_locs,
        )
        if (
            be_present,
            last_commit_info.author,
            last_loc,
            last_commit_info.hash,
            last_commit_info.modified_date,
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
    repo_nickname: str,
    repo_toe_lines: Dict[str, ToeLines],
) -> Tuple[Tuple[ToeLines, ToeLinesAttributesToUpdate], ...]:
    LOGGER_CONSOLE.info(
        "Getting non present toe lines to update",
        extra={
            "extra": {
                "repo_nickname": repo_nickname,
            }
        },
    )
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


def pull_repositories(
    tmpdir: str, group_name: str, optional_repo_nickname: Optional[str]
) -> None:
    make_group_dir(tmpdir, group_name)
    call_melts = [
        "CI=true",
        "CI_COMMIT_REF_NAME=master",
        "PROD_AWS_ACCESS_KEY_ID=$SERVICES_PROD_AWS_ACCESS_KEY_ID",
        "PROD_AWS_SECRET_ACCESS_KEY=$SERVICES_PROD_AWS_SECRET_ACCESS_KEY",
        f"melts drills --pull-repos {group_name}",
    ]
    if optional_repo_nickname:
        call_melts.append(f"--name {optional_repo_nickname}")
    os.system(" ".join(call_melts))  # nosec
    os.system(f"chmod -R +r {os.path.join(tmpdir, 'groups')}")  # nosec


async def refresh_active_root_repo_toe_lines(
    loaders: Dataloaders,
    group_name: str,
    group_path: str,
    root_repo: GitRootItem,
) -> None:
    LOGGER_CONSOLE.info(
        "Refreshing toe lines",
        extra={
            "extra": {
                "repo_nickname": root_repo.state.nickname,
            }
        },
    )
    try:
        repo = Repo(root_repo.state.nickname)
    except InvalidGitRepositoryError:
        LOGGER.error(
            "Invalid repository",
            extra={
                "extra": {
                    "group_name": group_name,
                    "repository": root_repo.state.nickname,
                }
            },
        )
        return
    except NoSuchPathError:
        LOGGER.error(
            "No such repository path",
            extra={
                "extra": {
                    "group_name": group_name,
                    "repository": root_repo.state.nickname,
                }
            },
        )
        return

    await git_utils.disable_quotepath(f"{root_repo.state.nickname}/.git")
    repo_toe_lines = {
        toe_lines.filename: toe_lines
        for toe_lines in await loaders.root_toe_lines.load_nodes(
            RootToeLinesRequest(group_name=group_name, root_id=root_repo.id)
        )
    }
    present_filenames = await get_present_filenames(
        group_path, repo, root_repo.state.nickname
    )
    present_toe_lines_to_add = await get_present_toe_lines_to_add(
        present_filenames,
        repo,
        root_repo.state.nickname,
        repo_toe_lines,
    )
    await collect(
        tuple(
            toe_lines_add(group_name, root_repo.id, filename, toe_lines_to_add)
            for filename, toe_lines_to_add in present_toe_lines_to_add
        ),
    )
    present_toe_lines_to_update = await get_present_toe_lines_to_update(
        present_filenames,
        repo,
        root_repo.state.nickname,
        repo_toe_lines,
    )
    await collect(
        tuple(
            toe_lines_update(current_value, attrs_to_update)
            for current_value, attrs_to_update in present_toe_lines_to_update
        ),
    )
    non_present_toe_lines_to_update = get_non_present_toe_lines_to_update(
        present_filenames,
        root_repo.state.nickname,
        repo_toe_lines,
    )
    await collect(
        tuple(
            toe_lines_update(current_value, attrs_to_update)
            for current_value, attrs_to_update in (
                non_present_toe_lines_to_update
            )
        ),
    )
    LOGGER_CONSOLE.info(
        "Finish refreshing toe lines",
        extra={
            "extra": {
                "repo_nickname": root_repo.state.nickname,
            }
        },
    )


async def refresh_inactive_root_repo_toe_lines(
    loaders: Dataloaders, group_name: str, root_repo: GitRootItem
) -> None:
    LOGGER_CONSOLE.info(
        "Refreshing inactive toe lines",
        extra={
            "extra": {
                "repo_nickname": root_repo.state.nickname,
            }
        },
    )
    repo_toe_lines = {
        toe_lines.filename: toe_lines
        for toe_lines in await loaders.root_toe_lines.load_nodes(
            RootToeLinesRequest(group_name=group_name, root_id=root_repo.id)
        )
    }
    present_filenames: Set[str] = set()
    non_present_toe_lines_to_update = get_non_present_toe_lines_to_update(
        present_filenames,
        root_repo.state.nickname,
        repo_toe_lines,
    )
    await collect(
        tuple(
            toe_lines_update(current_value, attrs_to_update)
            for current_value, attrs_to_update in (
                non_present_toe_lines_to_update
            )
        ),
    )
    LOGGER_CONSOLE.info(
        "Finish refreshing inactive toe lines",
        extra={
            "extra": {
                "repo_nickname": root_repo.state.nickname,
            }
        },
    )


@retry_on_exceptions(
    exceptions=(
        RepeatedToeLines,
        ToeLinesAlreadyUpdated,
    ),
    max_attempts=2,
)
async def refresh_root_repo_toe_lines(
    group_name: str, group_path: str, optional_repo_nickname: Optional[str]
) -> None:
    loaders = get_new_context()
    roots: Tuple[RootItem, ...] = await loaders.group_roots.load(group_name)
    active_root_repos = {
        root.state.nickname: root
        for root in roots
        if isinstance(root, GitRootItem) and root.state.status == "ACTIVE"
    }
    inactive_root_repos = {
        root.state.nickname: root
        for root in roots
        if isinstance(root, GitRootItem)
        and root.state.status == "INACTIVE"
        and root.state.nickname not in active_root_repos
    }
    await collect(
        tuple(
            refresh_active_root_repo_toe_lines(
                loaders, group_name, group_path, root_repo
            )
            for root_repo in active_root_repos.values()
            if not optional_repo_nickname
            or root_repo.state.nickname == optional_repo_nickname
        ),
        workers=3,
    )
    await collect(
        tuple(
            refresh_inactive_root_repo_toe_lines(
                loaders, group_name, root_repo
            )
            for root_repo in inactive_root_repos.values()
            if not optional_repo_nickname
            or root_repo.state.nickname == optional_repo_nickname
        ),
        workers=3,
    )


async def refresh_toe_lines(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    optional_repo_nickname: Optional[str] = (
        None if item.additional_info == "*" else item.additional_info
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        os.system("ulimit -n 4000")  # nosec
        os.system("ulimit -aS")  # nosec
        os.system("ulimit -aH")  # nosec
        os.chdir(tmpdir)
        pull_repositories(tmpdir, group_name, optional_repo_nickname)
        group_path = tmpdir + f"/groups/{group_name}"
        os.chdir(f"{group_path}/fusion")
        await refresh_root_repo_toe_lines(
            group_name, group_path, optional_repo_nickname
        )

    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
