# type: ignore

# pylint: disable=invalid-name
"""
Recover some credentials in some roots that where removed when updating the
root

Execution Time:    2022-06-17 at 23:24:02 UTC
Finalization Time: 2022-06-17 at 23:27:38 UTC
"""
from aioextensions import (
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.credentials.types import (
    Credential,
    CredentialItem,
    HttpsPatSecret,
    HttpsSecret,
    SshSecret,
)
from db_model.roots.types import (
    GitRoot,
)
from itertools import (
    chain,
)
import logging
import logging.config
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    Union,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

Secret = Union[HttpsSecret, HttpsPatSecret, SshSecret]


async def set_org_credential_to_roots(
    loaders: Dataloaders,
    organization_id: str,
    organization_name: str,
    credential_name: str,
    org_credentials: tuple[CredentialItem, ...],
) -> None:
    credential_roots = set(
        chain.from_iterable(
            [
                credential.state.roots
                for credential in org_credentials
                if credential.state.name == credential_name
            ]
        )
    )
    organization_roots = await loaders.organization_roots.load(
        organization_name
    )
    org_new_credentials: tuple[
        Credential, ...
    ] = await loaders.organization_credentials_new.load(organization_id)
    new_org_credential = next(
        (
            credential
            for credential in org_new_credentials
            if credential.state.name == credential_name
        ),
        None,
    )
    if new_org_credential:
        for organization_root in organization_roots:
            if (
                isinstance(organization_root, GitRoot)
                and organization_root.id in credential_roots
                and organization_root.state.credential_id is None
                and organization_root.state.credential_id
                != new_org_credential.id
            ):
                new_state = organization_root.state._replace(
                    credential_id=new_org_credential.id,
                    modified_by="aaguirre@fluidattacks.com",
                    modified_date=datetime_utils.get_iso_date(),
                )
                print(organization_name, "update", credential_name, new_state)
                # await roots_model.update_root_state(
                #     current_value=organization_root.state,
                #     group_name=organization_root.group_name,
                #     root_id=organization_root.id,
                #     state=new_state,
                # )


async def process_organization(
    loaders: Dataloaders,
    organization_id: str,
    organization_name: str,
    group_names: tuple[str, ...],
) -> None:
    groups_credentials: tuple[
        tuple[CredentialItem, ...], ...
    ] = await loaders.group_credentials.load_many(group_names)
    org_credentials = tuple(chain.from_iterable(groups_credentials))
    credential_names = {
        credential.state.name for credential in org_credentials
    }
    for credential_name in credential_names:
        await set_org_credential_to_roots(
            loaders,
            organization_id,
            organization_name,
            credential_name,
            org_credentials,
        )


async def main() -> None:  # noqa: MC0001
    loaders: Dataloaders = get_new_context()
    count = 0
    async for org_id, org_name, org_groups_names in (
        orgs_domain.iterate_organizations_and_groups(loaders)
    ):
        count += 1
        print(count, org_name)
        await process_organization(loaders, org_id, org_name, org_groups_names)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
