# pylint: disable=invalid-name
"""
Add welcome tour attribute to stakeholders

Execution Time:    2023-02-27 at 20:51:06 UTC
Finalization Time: 2023-02-27 at 20:51:22 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.credentials.types import (
    Credentials,
    OauthAzureSecret,
    OauthGithubSecret,
    OauthGitlabSecret,
)
from db_model.enums import (
    CredentialType,
)
from dynamodb import (
    keys,
    operations,
)
from organizations import (
    domain as orgs_domain,
)
import time


async def exist_new_name(
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
    )

    new_credential_name = (
        f'{str(oauth_credential.owner).split("@", maxsplit=1)[0]}'
        + f"({credential_provider})"
    )

    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["credentials_metadata"],
        values={
            "organization_id": oauth_credential.organization_id,
            "id": oauth_credential.organization_id,
        },
    )

    if exist_new_name(
        organization_credentials=organization_credentials,
        new_name=new_credential_name,
    ):
        raise Exception("Duplicated name found")

    print(f"changing {oauth_credential.state.name} to {new_credential_name}")
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item={"state.name": new_credential_name},
        key=primary_key,
        table=TABLE,
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
    async for org_id, org_name, _ in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        count += 1
        print(count, org_name)
        await process_organizations_credentials(org_id, loaders)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
