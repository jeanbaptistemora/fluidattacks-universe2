from aioextensions import (
    collect,
)
import asyncio
from dataloaders import (
    Dataloaders,
)
from db_model.organizations.types import (
    Organization,
    OrganizationUnreliableIndicatorsToUpdate,
)
from db_model.organizations.update import (
    update_unreliable_org_indicators,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
from git.cmd import (
    Git,
)
import json
import logging
from newutils.git_self import (
    pull_repositories,
)
from organizations.domain import (
    get_group_names,
)
import os
import tempfile

LOGGER = logging.getLogger(__name__)


def clone_mirrors(tmpdir: str, group: str) -> tuple[str, list[str]]:
    os.chdir(tmpdir)
    pull_repositories(
        tmpdir=tmpdir,
        group_name=group,
        optional_repo_nickname=None,
    )
    repositories_path = f"{tmpdir}/groups/{group}/fusion"
    os.chdir(repositories_path)
    repositories = [
        _dir for _dir in os.listdir(repositories_path) if os.path.isdir(_dir)
    ]

    return repositories_path, repositories


async def get_covered_nickname_commits(
    path: str, folder: str, group: str, git_root: GitRoot
) -> int:
    if folder != git_root.state.nickname:
        return 0

    Git().execute(
        [
            "git",
            "config",
            "--global",
            "--add",
            "safe.directory",
            os.path.join(path, folder),
        ]
    )
    proc = await asyncio.create_subprocess_exec(
        "git",
        "-C",
        os.path.join(path, folder),
        "rev-list",
        "--count",
        git_root.state.branch,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        return int(json.loads(stdout.decode()))

    LOGGER.error(
        "Error getting data over repository",
        extra={
            "extra": {
                "error": stderr.decode(),
                "group": group,
                "repository": folder,
            }
        },
    )

    return 0


async def get_covered_group_commits(
    path: str, folder: str, group: str, git_roots: tuple[GitRoot, ...]
) -> int:
    group_foder_coverted_commits: tuple[int, ...] = await collect(
        tuple(
            get_covered_nickname_commits(path, folder, group, git_root)
            for git_root in git_roots
        ),
        workers=2,
    )

    return sum(group_foder_coverted_commits)


async def update_organization_unreliable(
    *,
    organization: Organization,
    loaders: Dataloaders,
    progress: float,
    all_group_names: set[str],
) -> None:
    organization_group_names: tuple[str, ...] = await get_group_names(
        loaders, organization.id
    )
    organization_group_names = tuple(
        all_group_names.intersection(set(organization_group_names))
    )
    if not organization_group_names:
        await update_unreliable_org_indicators(
            organization_id=organization.id,
            organization_name=organization.name,
            indicators=OrganizationUnreliableIndicatorsToUpdate(
                covered_commits=0,
            ),
        )
        return

    groups_roots = await loaders.group_roots.load_many(
        organization_group_names
    )
    for group, roots in zip(organization_group_names, groups_roots):
        active_git_roots: tuple[GitRoot, ...] = tuple(
            root
            for root in roots
            if (
                isinstance(root, GitRoot)
                and root.state.status == RootStatus.ACTIVE
            )
        )
        LOGGER.info(
            "Updating covered commit stats for organization",
            extra={
                "extra": {
                    "organization_id": organization.id,
                    "organization_name": organization.name,
                    "progress": round(progress, 2),
                    "active_git_roots": len(active_git_roots),
                }
            },
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            clone_path, clone_repos = clone_mirrors(tmpdir=tmpdir, group=group)
            covered_organization_commits: tuple[int, ...] = await collect(
                (
                    get_covered_group_commits(
                        path=clone_path,
                        folder=repo,
                        group=group,
                        git_roots=active_git_roots,
                    )
                    for repo in clone_repos
                ),
                workers=2,
            )

        await update_unreliable_org_indicators(
            organization_id=organization.id,
            organization_name=organization.name,
            indicators=OrganizationUnreliableIndicatorsToUpdate(
                covered_commits=sum(covered_organization_commits),
            ),
        )
