from aioextensions import (
    collect,
)
import asyncio
from azure.devops.v6_0.git.models import (
    GitCommit,
    GitRepository,
    GitRepositoryStats,
)
from botocore.exceptions import (
    ClientError,
)
from dataloaders import (
    Dataloaders,
)
from db_model.azure_repositories.get import (
    get_repositories_stats,
)
from db_model.azure_repositories.types import (
    CredentialsGitRepository,
    CredentialsGitRepositoryCommit,
)
from db_model.azure_repositories.utils import (
    filter_urls,
)
from db_model.credentials.types import (
    Credentials,
)
from db_model.credentials.utils import (
    filter_pat_credentials,
)
from db_model.integration_repositories.remove import (
    remove,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from db_model.integration_repositories.update import (
    update_unreliable_repositories,
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
    Root,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from git.cmd import (
    Git,
)
import hashlib
from itertools import (
    chain,
)
import json
import logging
from newutils.datetime import (
    DEFAULT_ISO_STR,
    get_as_utc_iso_format,
    get_datetime_from_iso_str,
    get_now_minus_delta,
)
from newutils.git_self import (
    pull_repositories,
)
from organizations.domain import (
    get_group_names,
)
import os
import tempfile
from typing import (
    Optional,
)
from urllib.parse import (
    unquote_plus,
    urlparse,
)

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


def _get_id(repository: CredentialsGitRepository) -> str:
    return hashlib.sha256(
        repository.repository.web_url.lower().encode("utf-8")
    ).hexdigest()


def _get_branch(repository: CredentialsGitRepository) -> str:
    return str(
        repository.repository.default_branch
        if repository.repository.default_branch is not None
        else "main"
    )


async def _get_commit_date(
    *, loaders: Dataloaders, repository: CredentialsGitRepository
) -> str:
    git_commits: tuple[
        GitCommit, ...
    ] = await loaders.organization_integration_repositories_commits.load(
        CredentialsGitRepositoryCommit(
            credential=repository.credential,
            project_name=repository.repository.project.name,
            repository_id=repository.repository.id,
        )
    )

    if git_commits:
        return get_as_utc_iso_format(git_commits[0].committer.date)

    return DEFAULT_ISO_STR


async def _get_repository_count(
    *, repository: CredentialsGitRepository
) -> int:
    repo_stats: tuple[
        Optional[GitRepositoryStats], ...
    ] = await get_repositories_stats(
        repositories=tuple(
            [
                CredentialsGitRepositoryCommit(
                    credential=repository.credential,
                    project_name=repository.repository.project.name,
                    repository_id=repository.repository.id,
                )
            ]
        )
    )

    if repo_stats and repo_stats[0] is not None:
        return repo_stats[0].commits_count

    return 0


async def _update(
    *,
    organization_id: str,
    organization_name: str,
    repositories: tuple[CredentialsGitRepository, ...],
    repositories_stats: tuple[int, ...],
    repositories_dates: tuple[str, ...],
    covered_repositores: int,
) -> None:
    await collect(
        tuple(
            update_unreliable_repositories(
                repository=OrganizationIntegrationRepository(
                    id=_get_id(repository),
                    organization_id=organization_id,
                    branch=_get_branch(repository),
                    last_commit_date=date,
                    url=repository.repository.web_url,
                    commit_count=commit_count,
                )
            )
            for repository, date, commit_count in zip(
                repositories, repositories_dates, repositories_stats
            )
            if get_datetime_from_iso_str(date).timestamp()
            > get_now_minus_delta(days=60).timestamp()
        ),
        workers=4,
    )

    commit_counts = [
        commit_count
        for date, commit_count in zip(repositories_dates, repositories_stats)
        if get_datetime_from_iso_str(date).timestamp()
        > get_now_minus_delta(days=60).timestamp()
    ]
    await update_unreliable_org_indicators(
        organization_id=organization_id,
        organization_name=organization_name,
        indicators=OrganizationUnreliableIndicatorsToUpdate(
            missed_repositories=len(commit_counts),
            missed_commits=sum(commit_counts),
            covered_repositories=covered_repositores,
        ),
    )


async def _remove(
    *,
    organization_id: str,
    repositories: tuple[CredentialsGitRepository, ...],
    loaders: Dataloaders,
    repositories_dates: tuple[str, ...],
) -> None:
    repositories_ids: set[str] = {
        f"URL#{_get_id(repository)}#BRANCH#{_get_branch(repository).lower()}"
        for repository, date in zip(repositories, repositories_dates)
        if get_datetime_from_iso_str(date).timestamp()
        > get_now_minus_delta(days=60).timestamp()
    }
    current_unreliable_repositories: tuple[
        OrganizationIntegrationRepository, ...
    ] = await loaders.organization_unreliable_integration_repositories.load(
        (organization_id, None, None)
    )
    to_remove: tuple[OrganizationIntegrationRepository, ...] = tuple(
        repository
        for repository in current_unreliable_repositories
        if repository.id not in repositories_ids
    )

    await collect(
        tuple(remove(repository=repository) for repository in to_remove),
        workers=4,
    )


async def update_organization_repositories(  # pylint: disable=too-many-locals
    *,
    organization: Organization,
    loaders: Dataloaders,
    progress: float,
    all_group_names: set[str],
) -> None:
    organization_group_names: tuple[str, ...] = await get_group_names(
        loaders, organization.id
    )
    if not tuple(all_group_names.intersection(set(organization_group_names))):
        await update_unreliable_org_indicators(
            organization_id=organization.id,
            organization_name=organization.name,
            indicators=OrganizationUnreliableIndicatorsToUpdate(
                missed_repositories=0,
                missed_commits=0,
                covered_repositories=0,
            ),
        )
        return

    credentials: tuple[
        Credentials, ...
    ] = await loaders.organization_credentials.load(organization.id)
    pat_credentials: tuple[Credentials, ...] = filter_pat_credentials(
        credentials
    )
    all_repositories: tuple[
        tuple[GitRepository, ...], ...
    ] = await loaders.organization_integration_repositories.load_many(
        pat_credentials
    )
    groups_roots: tuple[
        tuple[Root, ...], ...
    ] = await loaders.group_roots.load_many(organization_group_names)
    roots: tuple[Root, ...] = tuple(chain.from_iterable(groups_roots))

    urls: set[str] = {
        unquote_plus(urlparse(root.state.url.lower()).path)
        for root in roots
        if isinstance(root, GitRoot)
    }
    active_urls: set[str] = {
        unquote_plus(urlparse(root.state.url.lower()).path)
        for root in roots
        if isinstance(root, GitRoot) and root.state.status == RootStatus.ACTIVE
    }
    repositories: tuple[CredentialsGitRepository, ...] = tuple(
        CredentialsGitRepository(
            credential=credential,
            repository=repository,
        )
        for credential, _repositories in zip(pat_credentials, all_repositories)
        for repository in _repositories
        if filter_urls(
            repository=repository,
            urls=urls,
        )
    )
    repositories_dates: tuple[str, ...] = await collect(
        tuple(
            _get_commit_date(loaders=loaders, repository=repository)
            for repository in repositories
        ),
        workers=1,
    )
    repositories_stats: tuple[int, ...] = await collect(
        tuple(
            _get_repository_count(repository=repository)
            for repository in repositories
        ),
        workers=1,
    )

    try:
        await _update(
            organization_id=organization.id,
            organization_name=organization.name,
            repositories=repositories,
            repositories_dates=repositories_dates,
            repositories_stats=repositories_stats,
            covered_repositores=len(active_urls),
        )
        await _remove(
            organization_id=organization.id,
            repositories=repositories,
            loaders=loaders,
            repositories_dates=repositories_dates,
        )

        LOGGER.info(
            "Organization integration repositories processed",
            extra={
                "extra": {
                    "organization_id": organization.id,
                    "organization_name": organization.name,
                    "progress": round(progress, 2),
                }
            },
        )
    except (ClientError, TypeError, UnavailabilityError) as ex:
        msg: str = (
            "Error: An error ocurred updating integration "
            "repositories in the database"
        )
        LOGGER.error(
            msg,
            extra={
                "extra": {
                    "organization_id": organization.id,
                    "organization_name": organization.name,
                    "ex": ex,
                }
            },
        )
