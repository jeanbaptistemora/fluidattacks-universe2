from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    in_thread,
)
from azure.devops.client import (
    AzureDevOpsAuthenticationError,
)
from azure.devops.connection import (
    Connection,
)
from azure.devops.exceptions import (
    AzureDevOpsClientRequestError,
    AzureDevOpsServiceError,
)
from azure.devops.v6_0.git.git_client import (
    GitClient,
)
from azure.devops.v6_0.git.models import (
    GitCommit,
    GitQueryCommitsCriteria,
    GitRepository,
    GitRepositoryStats,
)
from datetime import (
    timezone,
)
from dateutil import (
    parser,
)
from db_model.azure_repositories.types import (
    BasicRepoData,
    CredentialsGitRepositoryCommit,
)
from db_model.credentials.types import (
    Credentials,
    HttpsPatSecret,
)
from github import (
    GitCommit as GitHubCommit,
    Github,
)
import gitlab
from gitlab.const import (
    AccessLevel,
)
from itertools import (
    chain,
)
import logging
import logging.config
from msrest.authentication import (
    BasicAuthentication,
)
from settings import (
    LOGGING,
)
from typing import (
    Optional,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://dev.azure.com"


async def get_repositories(
    *,
    credentials: list[Credentials],
) -> list[list[GitRepository]]:
    return list(
        await collect(
            tuple(
                in_thread(
                    _get_repositories,
                    base_url=f"{BASE_URL}/"
                    f"{credential.state.azure_organization}",
                    access_token=credential.state.secret.token
                    if isinstance(credential.state.secret, HttpsPatSecret)
                    else "",
                )
                for credential in credentials
            ),
            workers=1,
        )
    )


def _get_repositories(
    *, base_url: str, access_token: str
) -> list[GitRepository]:
    credentials = BasicAuthentication("", access_token)
    connection = Connection(base_url=base_url, creds=credentials)
    try:
        git_client: GitClient = connection.clients.get_git_client()
        repositories: list[GitRepository] = git_client.get_repositories()
    except (
        AzureDevOpsClientRequestError,
        AzureDevOpsAuthenticationError,
        AzureDevOpsServiceError,
    ) as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
        return []
    else:
        return repositories


async def get_repositories_commits(
    *,
    repositories: list[CredentialsGitRepositoryCommit],
) -> list[list[GitCommit]]:
    repositories_commits = await collect(
        tuple(
            in_thread(
                _get_repositories_commits,
                organization=repository.credential.state.azure_organization,
                access_token=repository.credential.state.secret.token
                if isinstance(
                    repository.credential.state.secret, HttpsPatSecret
                )
                else "",
                repository_id=repository.repository_id,
                project_name=repository.project_name,
            )
            for repository in repositories
        ),
        workers=1,
    )

    return list(repositories_commits)


def _get_repositories_commits(
    *,
    organization: str,
    access_token: str,
    repository_id: str,
    project_name: str,
    total: bool = False,
) -> list[GitCommit]:
    credentials = BasicAuthentication("", access_token)
    connection = Connection(
        base_url=f"{BASE_URL}/{organization}", creds=credentials
    )
    try:
        git_client: GitClient = connection.clients_v6_0.get_git_client()
        commits: list[GitCommit] = git_client.get_commits(
            search_criteria=GitQueryCommitsCriteria()
            if total
            else GitQueryCommitsCriteria(top=1),
            repository_id=repository_id,
            project=project_name,
        )
    except (
        AzureDevOpsAuthenticationError,
        AzureDevOpsClientRequestError,
        AzureDevOpsServiceError,
    ) as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
        return []
    else:
        return commits


async def get_repositories_stats(
    *,
    repositories: tuple[CredentialsGitRepositoryCommit, ...],
) -> tuple[Optional[GitRepositoryStats], ...]:
    repositories_stats: tuple[
        Optional[GitRepositoryStats], ...
    ] = await collect(
        tuple(
            in_thread(
                _get_repositories_stats,
                organization=repository.credential.state.azure_organization,
                access_token=repository.credential.state.secret.token
                if isinstance(
                    repository.credential.state.secret, HttpsPatSecret
                )
                else "",
                repository_id=repository.repository_id,
                project_name=repository.project_name,
            )
            for repository in repositories
        ),
        workers=1,
    )

    return repositories_stats


def _get_repositories_stats(
    *,
    organization: str,
    access_token: str,
    repository_id: str,
    project_name: str,
) -> Optional[GitRepositoryStats]:
    credentials = BasicAuthentication("", access_token)
    connection = Connection(
        base_url=f"{BASE_URL}/{organization}", creds=credentials
    )
    try:
        git_client: GitClient = connection.clients_v6_0.get_git_client()
        stats: GitRepositoryStats = git_client.get_stats(
            repository_id=repository_id,
            project=project_name,
        )
    except (
        AzureDevOpsAuthenticationError,
        AzureDevOpsServiceError,
        AzureDevOpsClientRequestError,
    ) as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
        return None
    else:
        return stats


async def get_gitlab_commit_counts(
    *,
    token: str,
    projects: tuple[str, ...],
) -> tuple[int, ...]:

    return await collect(
        tuple(
            in_thread(
                _get_gitlab_commit_count, token=token, project_id=project_id
            )
            for project_id in projects
        ),
        workers=1,
    )


def _get_gitlab_commit_count(token: str, project_id: str) -> int:
    with gitlab.Gitlab(oauth_token=token) as g_session:
        project = g_session.projects.get(project_id, statistics=True)

        return project.attributes["statistics"]["commit_count"]


async def get_gitlab_commit(
    *,
    token: str,
    projects: tuple[str, ...],
) -> tuple[tuple[dict, ...], ...]:
    return await collect(
        tuple(
            in_thread(_get_gitlab_commit, token=token, project_id=project_id)
            for project_id in projects
        ),
        workers=1,
    )


def _get_gitlab_commit(token: str, project_id: str) -> tuple[dict, ...]:
    with gitlab.Gitlab(oauth_token=token) as g_session:
        project = g_session.projects.get(project_id)
        commits = project.commits.list(get_all=True, order_by="default")

        return tuple(commit.attributes for commit in commits)


async def get_gitlab_last_commit(
    *,
    token: str,
    projects: tuple[str, ...],
) -> tuple[tuple[dict, ...], ...]:
    return await collect(
        tuple(
            in_thread(
                _get_gitlab_last_commit, token=token, project_id=project_id
            )
            for project_id in projects
        ),
        workers=1,
    )


def _get_gitlab_last_commit(token: str, project_id: str) -> tuple[dict, ...]:
    with gitlab.Gitlab(oauth_token=token) as g_session:
        project = g_session.projects.get(project_id)
        commits = project.commits.list(per_page=1, page=1, order_by="default")

        return tuple(commit.attributes for commit in commits)


async def get_github_repos_commits(
    *, token: str, repositories: tuple[str, ...]
) -> tuple[tuple[GitHubCommit.GitCommit, ...], ...]:
    return await collect(
        tuple(
            in_thread(_get_github_repos_commits, token=token, repo_id=repo_id)
            for repo_id in repositories
        ),
        workers=1,
    )


def _get_github_repos_commits(
    token: str, repo_id: str
) -> tuple[GitHubCommit.GitCommit, ...]:
    commits: list[GitHubCommit.GitCommit] = []
    for commit in Github(token).get_repo(int(repo_id)).get_commits():
        commits.append(commit.commit)

    return tuple(commits)


async def get_github_repos(*, token: str) -> tuple[BasicRepoData, ...]:
    return await in_thread(_get_github_repos, token=token)


def _get_github_repos(token: str) -> tuple[BasicRepoData, ...]:
    repos: list[BasicRepoData] = []
    for org in Github(token).get_user().get_orgs():
        for repo in org.get_repos():
            repos.append(
                BasicRepoData(
                    id=str(repo.id),
                    remote_url=repo.clone_url,
                    ssh_url=repo.git_url,
                    web_url=repo.html_url,
                    branch=(
                        "refs/heads/"
                        f'{repo.default_branch.rstrip().lstrip("refs/heads/")}'
                    ),
                    last_activity_at=repo.updated_at.astimezone(timezone.utc),
                )
            )

    return tuple(repos)


async def get_gitlab_projects(*, token: str) -> tuple[BasicRepoData, ...]:
    return await in_thread(_get_gitlab_projects, token=token)


def _get_gitlab_projects(token: str) -> tuple[BasicRepoData, ...]:
    with gitlab.Gitlab(oauth_token=token) as g_session:
        groups = tuple(g_session.groups.list(all=True))
        group_projects = tuple(
            chain.from_iterable(
                tuple(
                    group.projects.list(
                        min_access_level=AccessLevel.REPORTER.value,
                    )
                    for group in groups
                )
            )
        )

        return tuple(
            BasicRepoData(
                id=gproject.id,
                remote_url=gproject.attributes["http_url_to_repo"],
                ssh_url=gproject.attributes["ssh_url_to_repo"],
                web_url=gproject.attributes["web_url"],
                branch=(
                    "refs/heads/"
                    + gproject.attributes["default_branch"]
                    .rstrip()
                    .lstrip("refs/heads/")
                ),
                last_activity_at=parser.parse(
                    gproject.attributes["last_activity_at"]
                ).astimezone(timezone.utc),
            )
            for gproject in group_projects
        )


class OrganizationRepositoriesLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        credentials: list[Credentials],
    ) -> list[list[GitRepository]]:
        return await get_repositories(credentials=credentials)


class OrganizationRepositoriesCommitsLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        repositories: list[CredentialsGitRepositoryCommit],
    ) -> list[list[GitCommit]]:
        return await get_repositories_commits(repositories=repositories)
