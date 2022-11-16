# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    in_thread,
)
from azure.devops.client import (
    AzureDevOpsAuthenticationError,
    AzureDevOpsServiceError,
)
from azure.devops.connection import (
    Connection,
)
from azure.devops.v6_0.git.git_client import (
    GitClient,
)
from azure.devops.v6_0.git.models import (
    GitCommit,
    GitQueryCommitsCriteria,
    GitRepository,
)
from azure_repositories.types import (
    CredentialsGitRepositoryCommit,
)
from db_model.credentials.types import (
    Credentials,
    HttpsPatSecret,
)
import logging
import logging.config
from msrest.authentication import (
    BasicAuthentication,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
BASE_URL = "https://dev.azure.com"


async def get_repositories(
    *,
    credentials: tuple[Credentials, ...],
) -> tuple[tuple[GitRepository, ...], ...]:
    return await collect(
        in_thread(
            _get_repositories,
            base_url=f"{BASE_URL}/{credential.state.azure_organization}",
            access_token=credential.state.secret.token
            if isinstance(credential.state.secret, HttpsPatSecret)
            else "",
        )
        for credential in credentials
    )


def _get_repositories(
    *, base_url: str, access_token: str
) -> tuple[GitRepository, ...]:
    credentials = BasicAuthentication("", access_token)
    connection = Connection(base_url=base_url, creds=credentials)
    try:
        git_client: GitClient = connection.clients.get_git_client()
        repositories: list[GitRepository] = git_client.get_repositories()
    except AzureDevOpsAuthenticationError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
        return tuple()
    else:
        return tuple(repositories)


async def get_repositories_commits(
    *,
    repositories: tuple[CredentialsGitRepositoryCommit, ...],
) -> tuple[tuple[GitCommit, ...], ...]:
    repositories_commits: tuple[tuple[GitCommit, ...], ...] = await collect(
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
        workers=2,
    )

    return repositories_commits


def _get_repositories_commits(
    *,
    organization: str,
    access_token: str,
    repository_id: str,
    project_name: str,
) -> tuple[GitCommit, ...]:
    credentials = BasicAuthentication("", access_token)
    connection = Connection(
        base_url=f"{BASE_URL}/{organization}", creds=credentials
    )
    try:
        git_client: GitClient = connection.clients.get_git_client()
        commits: list[GitCommit] = git_client.get_commits(
            search_criteria=GitQueryCommitsCriteria(top=1),
            repository_id=repository_id,
            project=project_name,
        )
    except (AzureDevOpsAuthenticationError, AzureDevOpsServiceError) as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
        return tuple()
    else:
        return tuple(commits)


class OrganizationRepositoriesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self,
        credentials: tuple[Credentials, ...],
    ) -> tuple[tuple[GitRepository, ...], ...]:
        return await get_repositories(credentials=credentials)


class OrganizationRepositoriesCommitsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self,
        repositories: tuple[CredentialsGitRepositoryCommit, ...],
    ) -> tuple[tuple[GitCommit, ...], ...]:
        return await get_repositories_commits(repositories=repositories)
