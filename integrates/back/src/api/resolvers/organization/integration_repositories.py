from aioextensions import (
    collect,
)
from azure.devops.v6_0.git.models import (
    GitRepository,
)
from dataloaders import (
    Dataloaders,
)
from db_model.azure_repositories.types import (
    CredentialsGitRepository,
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
from db_model.organizations.types import (
    Organization,
)
from db_model.roots.types import (
    GitRoot,
    Root,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.datetime import (
    get_now_minus_delta,
)
from urllib.parse import (
    unquote_plus,
    urlparse,
)


async def _get_repositories(
    *, loaders: Dataloaders, pat_credentials: list[Credentials]
) -> list[list[GitRepository]]:
    return await loaders.organization_integration_repositories.load_many(
        pat_credentials
    )


async def _get_roots(
    *, loaders: Dataloaders, organization_name: str
) -> set[str]:
    organization_roots: tuple[
        Root, ...
    ] = await loaders.organization_roots.load(organization_name)

    return {
        root.state.url
        for root in organization_roots
        if isinstance(root, GitRoot)
    }


async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[CredentialsGitRepository, ...]:
    loaders: Dataloaders = info.context.loaders
    credentials: tuple[
        Credentials, ...
    ] = await loaders.organization_credentials.load(parent.id)
    pat_credentials = list(filter_pat_credentials(credentials))
    repositories, roots_url = await collect(
        (
            _get_repositories(
                loaders=loaders, pat_credentials=pat_credentials
            ),
            _get_roots(loaders=loaders, organization_name=parent.name),
        )
    )
    urls = {
        unquote_plus(urlparse(url.lower()).path)
        for url in (roots_url if isinstance(roots_url, set) else set())
    }

    return tuple(
        CredentialsGitRepository(
            credential=credential,
            repository=repository,
        )
        for credential, _repositories in zip(pat_credentials, repositories)
        for repository in _repositories
        if repository.project.last_update_time.timestamp()
        > get_now_minus_delta(days=60).timestamp()
        and filter_urls(
            repository=repository,
            urls=urls,
        )
    )[:100]
