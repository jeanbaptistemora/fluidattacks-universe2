# pylint:disable=too-many-lines
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
from datetime import (
    datetime,
    timezone,
)
from dateutil import (
    parser,
)
from db_model.azure_repositories.get import (
    get_github_repos,
    get_github_repos_commits,
    get_gitlab_commit,
    get_gitlab_projects,
    get_repositories_stats,
)
from db_model.azure_repositories.types import (
    BasicRepoData,
    CredentialsGitRepository,
    CredentialsGitRepositoryCommit,
    ProjectStats,
    RepositoriesStats,
)
from db_model.azure_repositories.utils import (
    filter_urls,
)
from db_model.credentials.types import (
    Credentials,
    OauthGithubSecret,
    OauthGitlabSecret,
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
from git_self import (
    pull_repositories,
)
from github import (
    GitCommit as GitHubCommit,
)
import hashlib
from itertools import (
    chain,
)
import json
import logging
import logging.config
from newutils.datetime import (
    DEFAULT_ISO_STR,
    get_now_minus_delta,
    get_utc_now,
)
from oauth.gitlab import (
    get_token,
)
from organizations.domain import (
    get_group_names,
)
import os
import re
from settings import (
    LOGGING,
)
import tempfile
from typing import (
    Optional,
)
from urllib.parse import (
    unquote_plus,
    urlparse,
)

logging.config.dictConfig(LOGGING)

# Constants
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
    proc = await asyncio.create_subprocess_exec(
        "git",
        "-C",
        os.path.join(path, folder),
        "rev-list",
        "--count",
        git_root.state.branch,
        "--",
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


async def get_covered_nickname_authors(
    path: str, folder: str, group: str, git_root: GitRoot
) -> set[str]:
    proc = await asyncio.create_subprocess_exec(
        "git",
        "-C",
        os.path.join(path, folder),
        "shortlog",
        "-sne",
        git_root.state.branch,
        "--",
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        pattern = r"(?<=\<).+(?=\>)"
        authors = re.findall(pattern, stdout.decode())

        return set(author.lower() for author in authors)

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

    return set()


async def get_covered_nickname(
    path: str, folder: str, group: str, git_root: GitRoot
) -> tuple[int, set[str]]:
    if folder != git_root.state.nickname:
        return (0, set())

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

    return (
        await get_covered_nickname_commits(path, folder, group, git_root),
        await get_covered_nickname_authors(path, folder, group, git_root),
    )


async def get_covered_group(
    path: str, folder: str, group: str, git_roots: tuple[GitRoot, ...]
) -> tuple[int, set[str]]:
    group_foder_coverted: tuple[tuple[int, set[str]], ...] = await collect(
        tuple(
            get_covered_nickname(path, folder, group, git_root)
            for git_root in git_roots
        ),
        workers=1,
    )

    return (
        sum(commit for commit, _ in group_foder_coverted),
        set(
            set().union(*list(authors for _, authors in group_foder_coverted))
        ),
    )


async def get_pat_credentials_authors_stats(
    credentials: tuple[Credentials, ...],
    urls: set[str],
    loaders: Dataloaders,
) -> set[str]:
    pat_credentials: tuple[Credentials, ...] = filter_pat_credentials(
        credentials
    )
    all_repositories: tuple[
        tuple[GitRepository, ...], ...
    ] = await loaders.organization_integration_repositories.load_many(
        pat_credentials
    )
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
    repositories_dates: tuple[datetime, ...] = await collect(
        tuple(
            _get_commit_date(loaders=loaders, repository=repository)
            for repository in repositories
        ),
        workers=1,
    )
    repositories_authors: tuple[set[str], ...] = await collect(
        tuple(
            _get_missed_authors(loaders=loaders, repository=repository)
            for repository, date in zip(repositories, repositories_dates)
            if date.timestamp() > get_now_minus_delta(days=60).timestamp()
        ),
        workers=1,
    )

    return set().union(*list(repositories_authors))


async def get_gitlab_credentials_authors(
    *,
    credentials: tuple[Credentials, ...],
    urls: set[str],
    loaders: Dataloaders,
) -> set[str]:
    stats: tuple[ProjectStats, ...] = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    _get_gitlab_credential_stats(
                        credential=credential,
                        urls=urls,
                        loaders=loaders,
                    )
                    for credential in credentials
                ),
                workers=1,
            )
        )
    )
    filtered_stats: tuple[ProjectStats, ...] = tuple(
        {stat.project.id: stat for stat in stats}.values()
    )

    return {
        commit["author_email"].lower()
        for stat in filtered_stats
        for commit in stat.commits
    }


async def get_github_credentials_authors(
    *,
    credentials: tuple[Credentials, ...],
    urls: set[str],
) -> set[str]:
    stats: tuple[ProjectStats, ...] = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    _get_github_credential_stats(
                        credential=credential,
                        urls=urls,
                    )
                    for credential in credentials
                ),
                workers=1,
            )
        )
    )
    filtered_stats: tuple[ProjectStats, ...] = tuple(
        {stat.project.id: stat for stat in stats}.values()
    )

    return {
        commit["_rawData"]["author"]["email"].lower()
        for stat in filtered_stats
        for commit in stat.commits
    }


async def update_organization_unreliable(  # pylint: disable=too-many-locals
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
        all_group_names.intersection(
            set(group.lower() for group in organization_group_names)
        )
    )
    if not organization_group_names:
        await update_unreliable_org_indicators(
            organization_id=organization.id,
            organization_name=organization.name,
            indicators=OrganizationUnreliableIndicatorsToUpdate(
                covered_authors=0,
                covered_commits=0,
                missed_authors=0,
            ),
        )
        LOGGER.info(
            "Updated covered commit stats for organization",
            extra={
                "extra": {
                    "organization_id": organization.id,
                    "organization_name": organization.name,
                    "progress": round(progress, 2),
                    "active_git_roots": 0,
                    "covered_authors": 0,
                    "covered_commits": 0,
                }
            },
        )

        return

    groups_roots = await loaders.group_roots.load_many(
        organization_group_names
    )
    covered_organization: list[tuple[int, set[str]]] = []
    for group, roots in zip(organization_group_names, groups_roots):
        active_git_roots: tuple[GitRoot, ...] = tuple(
            root
            for root in roots
            if (
                isinstance(root, GitRoot)
                and root.state.status == RootStatus.ACTIVE
            )
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            clone_path, clone_repos = clone_mirrors(tmpdir=tmpdir, group=group)
            covered_group: tuple[tuple[int, set[str]], ...] = await collect(
                (
                    get_covered_group(
                        path=clone_path,
                        folder=repo,
                        group=group,
                        git_roots=active_git_roots,
                    )
                    for repo in clone_repos
                ),
                workers=1,
            )

            covered_organization.append(
                (
                    sum(commit for commit, _ in covered_group),
                    set(
                        set().union(
                            *list(authors for _, authors in covered_group)
                        )
                    ),
                )
            )

    credentials: tuple[
        Credentials, ...
    ] = await loaders.organization_credentials.load(organization.id)
    urls: set[str] = {
        unquote_plus(urlparse(root.state.url.lower()).path)
        for root in tuple(chain.from_iterable(groups_roots))
        if isinstance(root, GitRoot)
    }
    authors_stats: tuple[set[str], ...] = await collect(
        [
            get_pat_credentials_authors_stats(
                credentials=credentials,
                urls=urls,
                loaders=loaders,
            ),
            get_gitlab_credentials_authors(
                credentials=credentials,
                urls=urls,
                loaders=loaders,
            ),
            get_github_credentials_authors(
                credentials=credentials,
                urls=urls,
            ),
        ],
        workers=1,
    )

    await update_unreliable_org_indicators(
        organization_id=organization.id,
        organization_name=organization.name,
        indicators=OrganizationUnreliableIndicatorsToUpdate(
            covered_authors=len(
                set(
                    set().union(
                        *list(authors for _, authors in covered_organization)
                    )
                )
            ),
            missed_authors=len(set().union(*list(authors_stats))),
            covered_commits=sum(commit for commit, _ in covered_organization),
        ),
    )
    LOGGER.info(
        "Updated covered commit stats for organization",
        extra={
            "extra": {
                "organization_id": organization.id,
                "organization_name": organization.name,
                "progress": round(progress, 2),
                "active_git_roots": len(active_git_roots),
                "covered_commits": sum(
                    commit for commit, _ in covered_organization
                ),
                "covered_authors": len(
                    set(
                        set().union(
                            *list(
                                authors for _, authors in covered_organization
                            )
                        )
                    )
                ),
                "missed_authors": len(list(set().union(*list(authors_stats)))),
            }
        },
    )


def _get_id(repository: CredentialsGitRepository) -> str:
    return hashlib.sha256(
        repository.repository.web_url.lower().encode("utf-8")
    ).hexdigest()


def __get_id(url: str) -> str:
    return hashlib.sha256(url.lower().encode("utf-8")).hexdigest()


def _get_branch(repository: CredentialsGitRepository) -> str:
    return str(
        repository.repository.default_branch
        if repository.repository.default_branch is not None
        else "main"
    )


async def _get_missed_authors(
    *, loaders: Dataloaders, repository: CredentialsGitRepository
) -> set[str]:
    git_commits: tuple[
        GitCommit, ...
    ] = await loaders.organization_integration_repositories_commits.load(
        CredentialsGitRepositoryCommit(
            credential=repository.credential,
            project_name=repository.repository.project.name,
            repository_id=repository.repository.id,
            total=True,
        )
    )

    if git_commits:
        return {commit.author.email.lower() for commit in git_commits}

    return set()


async def _get_commit_date(
    *, loaders: Dataloaders, repository: CredentialsGitRepository
) -> datetime:
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
        return git_commits[0].committer.date

    return datetime.fromisoformat(DEFAULT_ISO_STR)


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
    repositories: tuple[RepositoriesStats, ...],
    covered_repositores: int,
) -> None:
    org_repositories: tuple[OrganizationIntegrationRepository, ...] = tuple(
        {
            repo.id: repo
            for repo in chain.from_iterable(
                repository.repositories for repository in repositories
            )
        }.values()
    )

    await collect(
        tuple(
            update_unreliable_repositories(repository=repository)
            for repository in org_repositories
        ),
        workers=4,
    )

    await update_unreliable_org_indicators(
        organization_id=organization_id,
        organization_name=organization_name,
        indicators=OrganizationUnreliableIndicatorsToUpdate(
            missed_repositories=sum(
                repository.missed_repositories for repository in repositories
            ),
            missed_commits=sum(
                repository.missed_commits for repository in repositories
            ),
            covered_repositories=covered_repositores,
        ),
    )


async def _remove(
    *,
    organization_id: str,
    valid_repositories_ids: set[str],
    loaders: Dataloaders,
) -> None:
    current_unreliable_repositories: tuple[
        OrganizationIntegrationRepository, ...
    ] = await loaders.organization_unreliable_integration_repositories.load(
        (organization_id, None, None)
    )
    to_remove: tuple[OrganizationIntegrationRepository, ...] = tuple(
        repository
        for repository in current_unreliable_repositories
        if repository.id not in valid_repositories_ids
    )

    await collect(
        tuple(remove(repository=repository) for repository in to_remove),
        workers=4,
    )


async def get_gitlab_credentials_stats(
    *,
    credentials: tuple[Credentials, ...],
    urls: set[str],
    loaders: Dataloaders,
    organization_id: str,
) -> RepositoriesStats:
    stats: tuple[ProjectStats, ...] = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    _get_gitlab_credential_stats(
                        credential=credential,
                        urls=urls,
                        loaders=loaders,
                    )
                    for credential in credentials
                ),
                workers=1,
            )
        )
    )
    filtered_stats: tuple[ProjectStats, ...] = tuple(
        {stat.project.id: stat for stat in stats}.values()
    )

    return RepositoriesStats(
        repositories=tuple(
            OrganizationIntegrationRepository(
                id=__get_id(stat.project.remote_url),
                organization_id=organization_id,
                branch=stat.project.branch,
                last_commit_date=parser.parse(
                    stat.commits[0]["committed_date"]
                ).astimezone(timezone.utc)
                if stat.commits
                else stat.project.last_activity_at,
                url=stat.project.remote_url,
                commit_count=len(stat.commits),
            )
            for stat in filtered_stats
        ),
        missed_repositories=len(filtered_stats),
        missed_commits=sum(len(stat.commits) for stat in filtered_stats),
    )


async def _get_gitlab_credential_stats(
    *,
    credential: Credentials,
    urls: set[str],
    loaders: Dataloaders,
) -> tuple[ProjectStats, ...]:
    if isinstance(credential.state.secret, OauthGitlabSecret):
        token: Optional[str] = credential.state.secret.access_token
        if credential.state.secret.valid_until <= get_utc_now():
            token = await get_token(
                credential=credential,
                loaders=loaders,
            )
        if not token:
            return tuple()

        projects: tuple[BasicRepoData, ...] = await get_gitlab_projects(
            token=token
        )
        filtered_projects = tuple(
            project
            for project in projects
            if project.last_activity_at.timestamp()
            > get_now_minus_delta(days=60).timestamp()
            and filter_urls(repository=project, urls=urls)
        )
        commits: tuple[tuple[dict, ...], ...] = await get_gitlab_commit(
            token=token,
            projects=tuple(project.id for project in filtered_projects),
        )
        sorted_commits: tuple[tuple[dict, ...], ...] = tuple(
            tuple(
                sorted(
                    p_commits, key=lambda x: x["committed_date"], reverse=True
                )
            )
            for p_commits in commits
        )
        return tuple(
            ProjectStats(
                project=project,
                commits=p_commits,
            )
            for project, p_commits in zip(filtered_projects, sorted_commits)
            if p_commits
            and parser.parse(p_commits[0]["committed_date"])
            .astimezone(timezone.utc)
            .timestamp()
            > get_now_minus_delta(days=60).timestamp()
        )

    return tuple()


async def get_github_credentials_stats(
    *,
    credentials: tuple[Credentials, ...],
    urls: set[str],
    organization_id: str,
) -> RepositoriesStats:
    stats: tuple[ProjectStats, ...] = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    _get_github_credential_stats(
                        credential=credential,
                        urls=urls,
                    )
                    for credential in credentials
                ),
                workers=1,
            )
        )
    )
    filtered_stats: tuple[ProjectStats, ...] = tuple(
        {stat.project.id: stat for stat in stats}.values()
    )

    return RepositoriesStats(
        repositories=tuple(
            OrganizationIntegrationRepository(
                id=__get_id(stat.project.remote_url),
                organization_id=organization_id,
                branch=stat.project.branch,
                last_commit_date=parser.parse(
                    stat.commits[0]["_rawData"]["committer"]["date"]
                ).astimezone(timezone.utc)
                if stat.commits
                else stat.project.last_activity_at,
                url=stat.project.remote_url,
                commit_count=len(stat.commits),
            )
            for stat in filtered_stats
        ),
        missed_repositories=len(filtered_stats),
        missed_commits=sum(len(stat.commits) for stat in filtered_stats),
    )


async def _get_github_credential_stats(
    *,
    credential: Credentials,
    urls: set[str],
) -> tuple[ProjectStats, ...]:
    if isinstance(credential.state.secret, OauthGithubSecret):
        token: str = credential.state.secret.access_token

        repositories: tuple[BasicRepoData, ...] = await get_github_repos(
            token=token
        )
        filtered_repositories = tuple(
            repository
            for repository in repositories
            if repository.last_activity_at.timestamp()
            > get_now_minus_delta(days=60).timestamp()
            and filter_urls(repository=repository, urls=urls)
        )
        commits: tuple[
            tuple[GitHubCommit.GitCommit, ...], ...
        ] = await get_github_repos_commits(
            token=token,
            repositories=tuple(
                repository.id for repository in filtered_repositories
            ),
        )
        sorted_commits: tuple[tuple[GitHubCommit.GitCommit, ...], ...] = tuple(
            tuple(
                sorted(p_commits, key=lambda x: x.committer.date, reverse=True)
            )
            for p_commits in commits
        )
        return tuple(
            ProjectStats(
                project=project,
                commits=tuple(commit.__dict__ for commit in p_commits),
            )
            for project, p_commits in zip(
                filtered_repositories, sorted_commits
            )
            if p_commits
            and p_commits[0].committer.date.timestamp()
            > get_now_minus_delta(days=60).timestamp()
        )

    return tuple()


async def get_pat_credentials_stats(
    credentials: tuple[Credentials, ...],
    urls: set[str],
    loaders: Dataloaders,
    organization_id: str,
) -> RepositoriesStats:
    pat_credentials: tuple[Credentials, ...] = filter_pat_credentials(
        credentials
    )
    all_repositories: tuple[
        tuple[GitRepository, ...], ...
    ] = await loaders.organization_integration_repositories.load_many(
        pat_credentials
    )
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
    repositories_dates: tuple[datetime, ...] = await collect(
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
    commit_counts = [
        commit_count
        for date, commit_count in zip(repositories_dates, repositories_stats)
        if date.timestamp() > get_now_minus_delta(days=60).timestamp()
    ]

    return RepositoriesStats(
        repositories=tuple(
            OrganizationIntegrationRepository(
                id=_get_id(repository),
                organization_id=organization_id,
                branch=_get_branch(repository),
                last_commit_date=date,
                url=repository.repository.web_url,
                commit_count=commit_count,
            )
            for repository, date, commit_count in zip(
                repositories, repositories_dates, repositories_stats
            )
            if date.timestamp() > get_now_minus_delta(days=60).timestamp()
        ),
        missed_repositories=len(commit_counts),
        missed_commits=sum(commit_counts),
    )


async def update_organization_repositories(
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
        all_group_names.intersection(
            set(group.lower() for group in organization_group_names)
        )
    )
    if not organization_group_names:
        await update_unreliable_org_indicators(
            organization_id=organization.id,
            organization_name=organization.name,
            indicators=OrganizationUnreliableIndicatorsToUpdate(
                missed_repositories=0,
                missed_commits=0,
                covered_repositories=0,
            ),
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

        return

    credentials: tuple[
        Credentials, ...
    ] = await loaders.organization_credentials.load(organization.id)
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
    repositories_stats: tuple[RepositoriesStats, ...] = await collect(
        [
            get_pat_credentials_stats(
                credentials=credentials,
                urls=urls,
                loaders=loaders,
                organization_id=organization.id,
            ),
            get_gitlab_credentials_stats(
                credentials=credentials,
                urls=urls,
                loaders=loaders,
                organization_id=organization.id,
            ),
            get_github_credentials_stats(
                credentials=credentials,
                urls=urls,
                organization_id=organization.id,
            ),
        ],
        workers=1,
    )

    try:
        await _update(
            organization_id=organization.id,
            organization_name=organization.name,
            repositories=repositories_stats,
            covered_repositores=len(active_urls),
        )
        await _remove(
            organization_id=organization.id,
            valid_repositories_ids={
                f"URL#{repository.id}#BRANCH#{repository.branch.lower()}"
                for stats in repositories_stats
                for repository in stats.repositories
            },
            loaders=loaders,
        )

        LOGGER.info(
            "Organization integration repositories processed",
            extra={
                "extra": {
                    "organization_id": organization.id,
                    "organization_name": organization.name,
                    "progress": round(progress, 2),
                    "covered_repositores": len(active_urls),
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
