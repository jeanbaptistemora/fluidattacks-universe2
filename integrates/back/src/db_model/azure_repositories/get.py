from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    in_thread,
)
from atlassian.bitbucket import (
    Cloud,
)
from atlassian.bitbucket.cloud.repositories.commits import (
    Commits,
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
from azure.devops.v6_0.accounts.accounts_client import (
    AccountsClient,
)
from azure.devops.v6_0.accounts.models import (
    Account,
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
from azure.devops.v6_0.profile.models import (
    Profile,
)
from azure.devops.v6_0.profile.profile_client import (
    ProfileClient,
)
from context import (
    FI_AZURE_OAUTH2_REPOSITORY_APP_ID,
    FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
)
from datetime import (
    datetime,
    timezone,
)
from dateutil import (
    parser,
)
from db_model.azure_repositories.types import (
    BasicRepoData,
    CredentialsGitRepositoryCommit,
    GitRepositoryCommit,
)
from db_model.credentials.types import (
    Credentials,
    HttpsPatSecret,
)
from github import (
    GitCommit as GitHubCommit,
    Github,
)
from github.GithubException import (
    BadCredentialsException,
)
import gitlab
from gitlab.const import (
    AccessLevel,
)
from gitlab.exceptions import (
    GitlabAuthenticationError,
)
from itertools import (
    chain,
)
import logging
import logging.config
from msrest.authentication import (
    BasicAuthentication,
    OAuthTokenAuthentication,
)
from settings import (
    LOGGING,
)
from typing import (
    Optional,
    Union,
)
from urllib3.util.url import (
    parse_url,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://dev.azure.com"
PROFILE_BASE_URL = "https://app.vssps.visualstudio.com"


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
    *, base_url: str, access_token: str, is_oauth: bool = False
) -> list[GitRepository]:
    credentials: Union[BasicAuthentication, OAuthTokenAuthentication]
    if is_oauth:
        credentials = OAuthTokenAuthentication(
            FI_AZURE_OAUTH2_REPOSITORY_APP_ID, {"access_token": access_token}
        )
    else:
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


async def get_oauth_repositories(
    *,
    token: str,
    accounts_names: tuple[str, ...],
) -> list[list[GitRepository]]:
    return list(
        await collect(
            tuple(
                in_thread(
                    _get_repositories,
                    base_url=f"{BASE_URL}/{account_name}",
                    access_token=token,
                    is_oauth=True,
                )
                for account_name in accounts_names
            ),
            workers=1,
        )
    )


async def get_bitbucket_commits(
    *, token: str, repos_ids: tuple[str, ...]
) -> tuple[tuple[Commits, ...], ...]:
    return await collect(
        tuple(
            in_thread(_get_bitbucket_commits, token=token, repo_id=repo_id)
            for repo_id in repos_ids
        )
    )


def _get_bitbucket_commits(*, token: str, repo_id: str) -> tuple[Commits, ...]:
    oauth2_dict = {
        "client_id": FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
        "token": {"access_token": token},
    }
    bitbucket_cloud = Cloud(oauth2=oauth2_dict)
    _workspace, _project_and_slug = repo_id.rsplit("#WORKSPACE#", 1)
    _project, _slug = _project_and_slug.rsplit("#PROJECT#", 1)
    workspace = bitbucket_cloud.workspaces.get(_workspace)
    project = workspace.projects.get(_project, "name")
    repo = project.repositories.get(_slug)

    commits: list[Commits] = []
    for commit in repo.commits.each():
        commits.append(commit)

    return tuple(commits)


async def get_bitbucket_repositories(
    *, token: str
) -> tuple[BasicRepoData, ...]:
    return await in_thread(_get_bitbucket_repositories, token=token)


def _get_bitbucket_repositories(*, token: str) -> tuple[BasicRepoData, ...]:
    repos: list[BasicRepoData] = []
    oauth2_dict = {
        "client_id": FI_BITBUCKET_OAUTH2_REPOSITORY_APP_ID,
        "token": {"access_token": token},
    }
    bitbucket_cloud = Cloud(oauth2=oauth2_dict)
    for workspace in bitbucket_cloud.workspaces.each():
        for project in workspace.projects.each():
            for repo in project.repositories.each():
                main_branch = repo.__dict__["_BitbucketBase__data"][
                    "mainbranch"
                ]["name"]
                default_branch = (
                    f'refs/heads/{main_branch.rstrip().lstrip("refs/heads/")}'
                )
                repos.append(
                    BasicRepoData(
                        id=(
                            f"{workspace.uuid}#WORKSPACE#"
                            f"{project.name}#PROJECT#{repo.slug}"
                        ),
                        remote_url=parse_url(
                            repo.__dict__["_BitbucketBase__data"]["links"][
                                "clone"
                            ][0]["href"],
                        )
                        ._replace(auth=None)
                        .url,
                        ssh_url=repo.__dict__["_BitbucketBase__data"]["links"][
                            "clone"
                        ][1]["href"],
                        web_url=repo.__dict__["_BitbucketBase__data"]["links"][
                            "html"
                        ]["href"],
                        branch=default_branch,
                        last_activity_at=datetime.fromisoformat(
                            "2000-01-01T05:00:00+00:00"
                        )
                        if repo.updated_on == "never updated"
                        else parser.parse(
                            repo.updated_on,
                        ).astimezone(timezone.utc),
                    )
                )

    return tuple(repos)


async def get_account_names(
    *,
    tokens: tuple[str, ...],
) -> tuple[tuple[str, ...], ...]:
    profiles: tuple[Profile, ...] = await collect(
        tuple(
            in_thread(
                _get_profile, base_url=PROFILE_BASE_URL, access_token=token
            )
            for token in tokens
        ),
        workers=1,
    )

    accounts = await collect(
        tuple(
            in_thread(
                _get_account,
                base_url=PROFILE_BASE_URL,
                access_token=token,
                public_alias=profile.additional_properties["publicAlias"],
            )
            for profile, token in zip(profiles, tokens)
        ),
        workers=1,
    )

    return tuple(
        tuple(account.account_name for account in _accounts)
        for _accounts in accounts
    )


def _get_account(
    *, base_url: str, access_token: str, public_alias: str
) -> tuple[Account, ...]:
    credentials = OAuthTokenAuthentication(
        FI_AZURE_OAUTH2_REPOSITORY_APP_ID, {"access_token": access_token}
    )
    connection = Connection(base_url=base_url, creds=credentials)
    try:
        account_client: AccountsClient = (
            connection.clients_v6_0.get_accounts_client()
        )
        account: list[Account] = account_client.get_accounts(
            None, public_alias
        )
    except (
        AzureDevOpsClientRequestError,
        AzureDevOpsAuthenticationError,
        AzureDevOpsServiceError,
    ) as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
        return tuple()
    else:
        return tuple(account)


def _get_profile(*, base_url: str, access_token: str) -> Profile:
    credentials = OAuthTokenAuthentication(
        FI_AZURE_OAUTH2_REPOSITORY_APP_ID, {"access_token": access_token}
    )
    connection = Connection(base_url=base_url, creds=credentials)
    try:
        profile_client: ProfileClient = (
            connection.clients_v6_0.get_profile_client()
        )
        profile: Profile = profile_client.get_profile("me")
    except (
        AzureDevOpsClientRequestError,
        AzureDevOpsAuthenticationError,
        AzureDevOpsServiceError,
    ) as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
        return None
    else:
        return profile


async def get_oauth_repositories_commits(
    *,
    repositories: list[GitRepositoryCommit],
) -> list[list[GitCommit]]:
    repositories_commits = await collect(
        tuple(
            in_thread(
                _get_repositories_commits,
                organization=repository.account_name,
                access_token=repository.access_token,
                repository_id=repository.repository_id,
                project_name=repository.project_name,
                is_oauth=True,
            )
            for repository in repositories
        ),
        workers=1,
    )

    return list(repositories_commits)


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
    is_oauth: bool = False,
) -> list[GitCommit]:
    credentials: Union[BasicAuthentication, OAuthTokenAuthentication]
    if is_oauth:
        credentials = OAuthTokenAuthentication(
            FI_AZURE_OAUTH2_REPOSITORY_APP_ID, {"access_token": access_token}
        )
    else:
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


async def get_oauth_repositories_stats(
    *,
    repositories: list[GitRepositoryCommit],
) -> tuple[Optional[GitRepositoryStats], ...]:
    repositories_stats: tuple[
        Optional[GitRepositoryStats], ...
    ] = await collect(
        tuple(
            in_thread(
                _get_repositories_stats,
                organization=repository.account_name,
                access_token=repository.access_token,
                repository_id=repository.repository_id,
                project_name=repository.project_name,
                is_oauth=True,
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
    is_oauth: bool = False,
) -> Optional[GitRepositoryStats]:
    credentials: Union[BasicAuthentication, OAuthTokenAuthentication]
    if is_oauth:
        credentials = OAuthTokenAuthentication(
            FI_AZURE_OAUTH2_REPOSITORY_APP_ID, {"access_token": access_token}
        )
    else:
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

    try:
        return await collect(
            tuple(
                in_thread(
                    _get_gitlab_commit_count,
                    token=token,
                    project_id=project_id,
                )
                for project_id in projects
            ),
            workers=1,
        )
    except GitlabAuthenticationError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
    return tuple()


def _get_gitlab_commit_count(token: str, project_id: str) -> int:
    with gitlab.Gitlab(oauth_token=token) as g_session:
        project = g_session.projects.get(project_id, statistics=True)

        return project.attributes["statistics"]["commit_count"]


async def get_gitlab_commit(
    *,
    token: str,
    projects: tuple[str, ...],
) -> tuple[tuple[dict, ...], ...]:
    try:
        return await collect(
            tuple(
                in_thread(
                    _get_gitlab_commit, token=token, project_id=project_id
                )
                for project_id in projects
            ),
            workers=1,
        )
    except GitlabAuthenticationError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
    return tuple()


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
    try:
        return await collect(
            tuple(
                in_thread(
                    _get_gitlab_last_commit, token=token, project_id=project_id
                )
                for project_id in projects
            ),
            workers=1,
        )
    except GitlabAuthenticationError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
    return tuple()


def _get_gitlab_last_commit(token: str, project_id: str) -> tuple[dict, ...]:
    with gitlab.Gitlab(oauth_token=token) as g_session:
        project = g_session.projects.get(project_id)
        commits = project.commits.list(per_page=1, page=1, order_by="default")

        return tuple(commit.attributes for commit in commits)


async def get_github_repos_commits(
    *, token: str, repositories: tuple[str, ...]
) -> tuple[tuple[GitHubCommit.GitCommit, ...], ...]:
    try:
        return await collect(
            tuple(
                in_thread(
                    _get_github_repos_commits, token=token, repo_id=repo_id
                )
                for repo_id in repositories
            ),
            workers=1,
        )
    except BadCredentialsException as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
    return tuple()


def _get_github_repos_commits(
    token: str, repo_id: str
) -> tuple[GitHubCommit.GitCommit, ...]:
    commits: list[GitHubCommit.GitCommit] = []
    for commit in Github(token).get_repo(int(repo_id)).get_commits():
        commits.append(commit.commit)

    return tuple(commits)


async def get_github_repos(*, token: str) -> tuple[BasicRepoData, ...]:
    try:
        return await in_thread(_get_github_repos, token=token)
    except BadCredentialsException as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
    return tuple()


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
    try:
        return await in_thread(_get_gitlab_projects, token=token)
    except GitlabAuthenticationError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
    return tuple()


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
