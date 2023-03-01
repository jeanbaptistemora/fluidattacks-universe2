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
from batch_dispatch.utils.s3 import (
    download_repo,
)
from custom_exceptions import (
    RepeatedToeLines,
    ToeLinesAlreadyUpdated,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
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
)
from git.objects.blob import (
    Blob,
)
from git.repo import (
    Repo,
)
import git_self as git_utils
import logging
import logging.config
from newutils import (
    files as files_utils,
)
import os
from os import (
    path,
)
from roots.domain import (
    get_root_id_by_nickname,
)
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


async def get_present_filenames(repo: Repo, repo_nickname: str) -> set[str]:
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
        str(tree.path) for tree in trees if isinstance(tree, Blob)
    )
    file_exists = await collect(
        in_thread(os.path.exists, path.join(str(repo.working_dir), filename))
        for filename in included_head_filenames
    )

    file_islink = await collect(
        in_thread(os.path.islink, path.join(str(repo.working_dir), filename))
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
    present_filenames: set[str],
    repo: Repo,
    repo_nickname: str,
    repo_toe_lines: dict[str, ToeLines],
) -> tuple[tuple[str, ToeLinesAttributesToAdd], ...]:
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
            files_get_lines_count(path.join(str(repo.working_dir), filename))
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
                last_commit_date=last_commit_info.modified_date,
            ),
        )
        for (filename, last_commit_info, last_loc,) in zip(
            non_db_filenames,
            last_commit_infos,
            last_locs,
        )
    )


async def get_present_toe_lines_to_update(
    present_filenames: set[str],
    repo: Repo,
    repo_nickname: str,
    repo_toe_lines: dict[str, ToeLines],
) -> tuple[tuple[ToeLines, ToeLinesAttributesToUpdate], ...]:
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
            files_get_lines_count(path.join(str(repo.working_dir), filename))
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
                last_commit_date=last_commit_info.modified_date,
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
            repo_toe_lines[filename].state.be_present,
            repo_toe_lines[filename].state.last_author,
            repo_toe_lines[filename].state.loc,
            repo_toe_lines[filename].state.last_commit,
            repo_toe_lines[filename].state.last_commit_date,
        )
    )


def get_non_present_toe_lines_to_update(
    present_filenames: set[str],
    repo_nickname: str,
    repo_toe_lines: dict[str, ToeLines],
) -> tuple[tuple[ToeLines, ToeLinesAttributesToUpdate], ...]:
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
        and repo_toe_lines[db_filename].state.be_present
    )


async def refresh_active_root_repo_toe_lines(
    loaders: Dataloaders, git_root: GitRoot, repo: Repo
) -> None:
    LOGGER.info(
        "Refreshing toe lines",
        extra={
            "extra": {
                "repo_nickname": git_root.state.nickname,
            }
        },
    )
    await git_utils.disable_quotepath(path.join(str(repo.working_dir), ".git"))
    present_filenames = await get_present_filenames(
        repo, git_root.state.nickname
    )

    repo_toe_lines = {
        toe_lines.filename: toe_lines
        for toe_lines in await loaders.root_toe_lines.load_nodes(
            RootToeLinesRequest(
                group_name=git_root.group_name, root_id=git_root.id
            )
        )
    }
    present_toe_lines_to_add = await get_present_toe_lines_to_add(
        present_filenames,
        repo,
        git_root.state.nickname,
        repo_toe_lines,
    )
    await collect(
        tuple(
            toe_lines_add(
                loaders,
                git_root.group_name,
                git_root.id,
                filename,
                toe_lines_to_add,
                is_moving_toe_lines=True,
            )
            for filename, toe_lines_to_add in present_toe_lines_to_add
        ),
    )
    present_toe_lines_to_update = await get_present_toe_lines_to_update(
        present_filenames,
        repo,
        git_root.state.nickname,
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
        git_root.state.nickname,
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
                "repo_nickname": git_root.state.nickname,
            }
        },
    )


async def refresh_inactive_root_repo_toe_lines(
    loaders: Dataloaders, git_root: GitRoot
) -> None:
    LOGGER.info(
        "Refreshing inactive toe lines",
        extra={
            "extra": {
                "repo_nickname": git_root.state.nickname,
            }
        },
    )
    repo_toe_lines = {
        toe_lines.filename: toe_lines
        for toe_lines in await loaders.root_toe_lines.load_nodes(
            RootToeLinesRequest(
                group_name=git_root.group_name, root_id=git_root.id
            )
        )
    }
    present_filenames: set[str] = set()
    non_present_toe_lines_to_update = get_non_present_toe_lines_to_update(
        present_filenames,
        git_root.state.nickname,
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
                "repo_nickname": git_root.state.nickname,
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
    loaders: Dataloaders, git_root: GitRoot, repo: Repo
) -> None:
    if git_root.state.status == RootStatus.ACTIVE:
        await refresh_active_root_repo_toe_lines(loaders, git_root, repo)
    elif git_root.state.status == RootStatus.INACTIVE:
        await refresh_inactive_root_repo_toe_lines(loaders, git_root)


async def refresh_toe_lines(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    repo_nickname: str | None = (
        None if item.additional_info == "*" else item.additional_info
    )
    loaders = get_new_context()
    roots = [
        root
        for root in await loaders.group_roots.load(group_name)
        if isinstance(root, GitRoot)
    ]
    if repo_nickname:
        root_id = get_root_id_by_nickname(repo_nickname, roots, True)
        roots = [root for root in roots if root.id == root_id]
    for git_root in roots:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = path.join(tmpdir, git_root.state.nickname)
            downloaded = await download_repo(group_name, git_root, tmpdir)
            if not downloaded:
                continue
            repo = Repo(repo_path)
            await refresh_root_repo_toe_lines(loaders, git_root, repo)

    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
