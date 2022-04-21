from aioextensions import (
    collect,
    in_thread,
)
from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
from custom_exceptions import (
    RepeatedToeLines,
    ToeLinesAlreadyUpdated,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
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


async def get_present_filenames(repo: Repo, repo_nickname: str) -> Set[str]:
    LOGGER.info(
        "Getting present filenames",
        extra={
            "extra": {
                "repo_nickname": repo_nickname,
            }
        },
    )
    trees = repo.head.commit.tree.traverse()
    included_head_filenames = tuple(
        tree.path for tree in trees if tree.type == "blob"
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


async def get_present_toe_lines_to_add(
    present_filenames: Set[str],
    repo: Repo,
    repo_nickname: str,
    repo_toe_lines: Dict[str, ToeLines],
) -> Tuple[Tuple[str, ToeLinesAttributesToAdd], ...]:
    LOGGER.info(
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
        workers=1024,
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
                attacked_at=None,
                attacked_by="",
                attacked_lines=0,
                last_author=last_commit_info.author,
                comments="",
                loc=last_loc,
                last_commit=last_commit_info.hash,
                modified_date=last_commit_info.modified_date,
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
    LOGGER.info(
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
        workers=1024,
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
                last_author=last_commit_info.author,
                loc=last_loc,
                last_commit=last_commit_info.hash,
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
            repo_toe_lines[filename].last_author,
            repo_toe_lines[filename].loc,
            repo_toe_lines[filename].last_commit,
            repo_toe_lines[filename].modified_date,
        )
    )


def get_non_present_toe_lines_to_update(
    present_filenames: Set[str],
    repo_nickname: str,
    repo_toe_lines: Dict[str, ToeLines],
) -> Tuple[Tuple[ToeLines, ToeLinesAttributesToUpdate], ...]:
    LOGGER.info(
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
    group_dir = os.path.join(tmpdir, "groups", group_name, "fusion")
    os.makedirs(group_dir, exist_ok=True)


def pull_repositories(
    tmpdir: str, group_name: str, optional_repo_nickname: Optional[str]
) -> None:
    make_group_dir(tmpdir, group_name)
    call_melts = [
        "CI=true",
        "CI_COMMIT_REF_NAME=master",
        "PROD_AWS_ACCESS_KEY_ID=$PROD_SERVICES_AWS_ACCESS_KEY_ID",
        "PROD_AWS_SECRET_ACCESS_KEY=$PROD_SERVICES_AWS_SECRET_ACCESS_KEY",
        f"melts drills --pull-repos {group_name}",
    ]
    if optional_repo_nickname:
        call_melts.append(f"--name {optional_repo_nickname}")
    os.system(" ".join(call_melts))  # nosec
    os.system(f"chmod -R +r {os.path.join(tmpdir, 'groups')}")  # nosec


async def refresh_active_root_repo_toe_lines(
    loaders: Dataloaders,
    group_name: str,
    root_repo: GitRootItem,
) -> None:
    LOGGER.info(
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
    try:
        repo_branch = getattr(repo.heads, root_repo.state.branch)
        repo_branch.checkout()
    except AttributeError:
        LOGGER.error(
            "Branch not found",
            extra={
                "extra": {
                    "branch": root_repo.state.branch,
                    "group_name": group_name,
                    "repository": root_repo.state.nickname,
                }
            },
        )
        present_filenames = set()
    else:
        present_filenames = await get_present_filenames(
            repo, root_repo.state.nickname
        )

    repo_toe_lines = {
        toe_lines.filename: toe_lines
        for toe_lines in await loaders.root_toe_lines.load_nodes(
            RootToeLinesRequest(group_name=group_name, root_id=root_repo.id)
        )
    }
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
    LOGGER.info(
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
    LOGGER.info(
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
    LOGGER.info(
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
    max_attempts=3,
)
async def refresh_root_repo_toe_lines(
    group_name: str, optional_repo_nickname: Optional[str]
) -> None:
    loaders = get_new_context()
    roots: Tuple[RootItem, ...] = await loaders.group_roots.load(group_name)
    # There are roots with the same nickname
    # then it is going to take the last modified root
    sorted_roots = sorted(
        roots,
        key=lambda root: datetime.fromisoformat(root.state.modified_date),
    )
    active_root_repos = {
        root.state.nickname: root
        for root in sorted_roots
        if isinstance(root, GitRootItem) and root.state.status == "ACTIVE"
    }
    # Deactivate all the toe lines for all the inactive roots
    # with the same nickname
    inactive_root_repos = tuple(
        root
        for root in sorted_roots
        if isinstance(root, GitRootItem)
        and root.state.status == "INACTIVE"
        and root.state.nickname not in active_root_repos
    )
    active_root_repos_to_proccess = tuple(
        root_repo
        for root_repo in active_root_repos.values()
        if not optional_repo_nickname
        or root_repo.state.nickname == optional_repo_nickname
    )
    for root_repo in active_root_repos_to_proccess:
        await refresh_active_root_repo_toe_lines(
            loaders, group_name, root_repo
        )
    inactive_root_repos_to_proccess = tuple(
        root_repo
        for root_repo in inactive_root_repos
        if not optional_repo_nickname
        or root_repo.state.nickname == optional_repo_nickname
    )
    for root_repo in inactive_root_repos_to_proccess:
        await refresh_inactive_root_repo_toe_lines(
            loaders, group_name, root_repo
        )


async def refresh_toe_lines(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    optional_repo_nickname: Optional[str] = (
        None if item.additional_info == "*" else item.additional_info
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        pull_repositories(tmpdir, group_name, optional_repo_nickname)
        group_path = tmpdir + f"/groups/{group_name}"
        os.chdir(f"{group_path}/fusion")
        await refresh_root_repo_toe_lines(group_name, optional_repo_nickname)

    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
