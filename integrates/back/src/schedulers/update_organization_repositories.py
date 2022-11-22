# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
from azure.devops.v6_0.git.models import (
    GitCommit,
    GitRepository,
)
from azure_repositories.types import (
    CredentialsGitRepository,
    CredentialsGitRepositoryCommit,
)
from azure_repositories.utils import (
    filter_urls,
)
from botocore.exceptions import (
    ClientError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
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
from db_model.organizations.get import (
    get_all_organizations,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.roots.types import (
    GitRoot,
    Root,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
import hashlib
from itertools import (
    chain,
)
from newutils.datetime import (
    DEFAULT_ISO_STR,
    get_as_utc_iso_format,
    get_datetime_from_iso_str,
    get_now_minus_delta,
)
from operator import (
    attrgetter,
)
from organizations.domain import (
    get_all_active_group_names,
    get_group_names,
)
from schedulers.common import (
    error,
    info,
)
from urllib.parse import (
    unquote_plus,
    urlparse,
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


async def _update(
    *,
    organization_id: str,
    repositories: tuple[CredentialsGitRepository, ...],
    repositories_dates: tuple[str, ...],
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
                    commit_count=0,
                )
            )
            for repository, date in zip(repositories, repositories_dates)
            if get_datetime_from_iso_str(date).timestamp()
            > get_now_minus_delta(days=60).timestamp()
        ),
        workers=4,
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
    if not tuple(all_group_names.intersection(set(organization_group_names))):
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

    try:
        await _update(
            organization_id=organization.id,
            repositories=repositories,
            repositories_dates=repositories_dates,
        )
        await _remove(
            organization_id=organization.id,
            repositories=repositories,
            loaders=loaders,
            repositories_dates=repositories_dates,
        )

        info(
            "Organization integration repositories processed",
            extra={
                "organization_id": organization.id,
                "organization_name": organization.name,
                "progress": round(progress, 2),
            },
        )
    except (ClientError, TypeError, UnavailabilityError) as ex:
        msg: str = (
            "Error: An error ocurred updating integration "
            "repositories in the database"
        )
        error(
            msg,
            extra={
                "organization_id": organization.id,
                "organization_name": organization.name,
                "ex": ex,
            },
        )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    organizations: tuple[Organization, ...] = await get_all_organizations()
    all_group_names: set[str] = set(await get_all_active_group_names(loaders))
    organizations_sorted_by_name = sorted(
        organizations, key=attrgetter("name")
    )
    len_gorganizations_sorted_by_name = len(organizations_sorted_by_name)

    await collect(
        tuple(
            update_organization_repositories(
                organization=organization,
                loaders=loaders,
                progress=count / len_gorganizations_sorted_by_name,
                all_group_names=all_group_names,
            )
            for count, organization in enumerate(organizations_sorted_by_name)
        ),
        workers=1,
    )
