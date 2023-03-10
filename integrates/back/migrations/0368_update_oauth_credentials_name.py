# pylint: disable=invalid-name
"""
Update credentials name to a new format

Execution Time:    2023-03-10 at 22:18:59 UTC
Finalization Time: 2023-03-10 at 22:19:26 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    OauthAzureSecret,
    OauthBitbucketSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
)
from db_model.credentials.update import (
    update_credential_state,
)
from db_model.enums import (
    CredentialType,
)
from organizations import (
    domain as orgs_domain,
)
import time
from typing import (
    Any,
)


def exist_new_name(
    organization_credentials: list[Credentials], new_name: str
) -> bool:
    return any(
        credential.state.name == new_name
        for credential in organization_credentials
    )


async def process_oauth_credential(
    organization_credentials: list[Credentials],
    oauth_credential: Credentials,
) -> None:
    credential_provider = (
        "GitLab"
        if isinstance(oauth_credential.state.secret, OauthGitlabSecret)
        else "GitHub"
        if isinstance(oauth_credential.state.secret, OauthGithubSecret)
        else "Azure"
        if isinstance(oauth_credential.state.secret, OauthAzureSecret)
        else "Bitbucket"
        if isinstance(oauth_credential.state.secret, OauthBitbucketSecret)
        else None
    )
    if not credential_provider:
        return None

    new_credential_name = (
        f'{str(oauth_credential.owner).split("@", maxsplit=1)[0]}'
        + f"({credential_provider})"
    )

    if exist_new_name(
        organization_credentials=organization_credentials,
        new_name=new_credential_name,
    ):
        print("[ERROR] Duplicated name found")

    print(f"changing {oauth_credential.state.name} to {new_credential_name}")

    await update_credential_state(
        current_value=oauth_credential.state,
        organization_id=oauth_credential.organization_id,
        credential_id=oauth_credential.id,
        state=oauth_credential.state._replace(
            modified_by="faristizabal@fluidattacks.com",
            modified_date=datetime.utcnow(),
            name=new_credential_name,
        ),
    )


async def process_organizations_credentials(
    organization_id: str,
    loaders: Dataloaders,
) -> None:
    org_credentials = await loaders.organization_credentials.load(
        organization_id
    )
    oauth_credentials = [
        credential
        for credential in org_credentials
        if credential.state.type == CredentialType.OAUTH
        and credential.state.name
        != (
            f'{str(credential.owner).split("@", maxsplit=1)[0]}'
            + f'({"GitLab" or "GitHub" or "Azure" or "Bitbucket"})'
        )
    ]
    await collect(
        tuple(
            process_oauth_credential(
                organization_credentials=org_credentials,
                oauth_credential=oauth_credential,
            )
            for oauth_credential in oauth_credentials
        ),
        workers=100,
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    count = 0
    futures: Any = []
    async for org in (orgs_domain.iterate_organizations()):
        count += 1
        print(count, org.name)
        futures.append(process_organizations_credentials(org.id, loaders))
    await collect(futures, workers=10)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
