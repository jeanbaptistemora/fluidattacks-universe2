# type: ignore

# pylint: disable=invalid-name
"""
Move the group credentials information into the organization credentials

Execution Time:    2022-06-13 at 14:53:02 UTC
Finalization Time: 2022-06-13 at 15:12:32 UTC

Execution Time:    2022-06-14 at 17:56:08 UTC
Finalization Time: 2022-06-14 at 17:59:56 UTC
"""
from aioextensions import (
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model import (
    credentials as credentials_model,
    roots as roots_model,
    TABLE,
)
from db_model.credentials.types import (
    Credential,
    CredentialItem,
    CredentialNewState,
    CredentialState,
    HttpsPatSecret,
    HttpsSecret,
    SshSecret,
)
from db_model.enums import (
    CredentialType,
)
from db_model.roots.types import (
    GitRoot,
)
from dynamodb import (
    keys,
    operations,
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
    cast,
)
from uuid import (
    uuid4,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")

Secret = HttpsSecret | HttpsPatSecret | SshSecret


def _get_secret_info(
    last_credential: CredentialItem,
) -> Secret:
    secret: Secret = (
        SshSecret(key=last_credential.state.key or "")
        if last_credential.metadata.type is CredentialType.SSH
        else HttpsPatSecret(token=last_credential.state.token or "")
        if last_credential.state.token
        else HttpsSecret(
            user=last_credential.state.user or "",
            password=last_credential.state.password or "",
        )
    )
    return secret


async def _update_owner(credential: Credential, owner: str) -> None:
    key_structure = TABLE.primary_key
    credential_key = keys.build_key(
        facet=TABLE.facets["credentials_new_metadata"],
        values={
            "organization_id": credential.organization_id,
            "id": credential.id,
        },
    )
    credential_item = {"owner": owner}
    await operations.update_item(
        condition_expression=(Attr(key_structure.partition_key).exists()),
        item=credential_item,
        key=credential_key,
        table=TABLE,
    )


async def add_org_credential(  # pylint: disable=too-many-locals
    loaders: Dataloaders,
    organization_id: str,
    organization_name: str,
    credential_name: str,
    org_credentials: tuple[CredentialItem, ...],
) -> None:
    kospina_email = "kospina@fluidattacks.com"
    ccarrasco_email = "ccarrasco@fluidattacks.com"
    org_new_credentials: tuple[
        Credential, ...
    ] = await loaders.organization_credentials_new.load(organization_id)

    group_credentials_with_the_same_name = tuple(
        credential
        for credential in org_credentials
        if credential.state.name == credential_name
    )
    group_credentials_ids_with_the_same_name = tuple(
        credential.id
        for credential in org_credentials
        if credential.state.name == credential_name
    )
    historics = cast(
        tuple[tuple[CredentialState, ...], ...],
        await loaders.credential_historic_state.load_many(
            group_credentials_ids_with_the_same_name
        ),
    )
    older_states: list[CredentialState] = []
    newest_states: list[CredentialState] = []
    for hictoric in historics:
        older_state = min(
            hictoric,
            key=lambda state: datetime.fromisoformat(state.modified_date),
        )
        older_states.append(older_state)
        newest_state = max(
            hictoric,
            key=lambda state: datetime.fromisoformat(state.modified_date),
        )
        newest_states.append(newest_state)

    owner = older_states[0].modified_by
    if next(
        (
            older_state
            for older_state in older_states
            if older_state.modified_by == kospina_email
        ),
        None,
    ):
        owner = kospina_email
    if next(
        (
            older_state
            for older_state in older_states
            if older_state.modified_by == ccarrasco_email
        ),
        None,
    ):
        owner = ccarrasco_email

    for state in older_states:
        if state.modified_by != owner and owner not in {
            kospina_email,
            ccarrasco_email,
        }:
            raise Exception(f"Unhandled owner in {organization_name}")

    current_new_org_cred = next(
        (
            credential
            for credential in org_new_credentials
            if credential.state.name == credential_name
        ),
        None,
    )
    if current_new_org_cred and current_new_org_cred.owner != owner:
        await _update_owner(current_new_org_cred, owner)

    if not current_new_org_cred:
        last_credential = max(
            group_credentials_with_the_same_name,
            key=lambda credential: datetime.fromisoformat(
                credential.state.modified_date
            ),
        )

        new_credential = Credential(
            id=str(uuid4()),
            organization_id=organization_id,
            owner=owner,
            state=CredentialNewState(
                modified_by=last_credential.state.modified_by,
                modified_date=last_credential.state.modified_date,
                name=last_credential.state.name,
                secret=_get_secret_info(last_credential),
                type=last_credential.metadata.type,
            ),
        )
        await credentials_model.add_new(credential=new_credential)
        loaders.organization_credentials_new.clear(organization_id)


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
                and organization_root.state.credential_id
                != new_org_credential.id
            ):
                new_state = organization_root.state._replace(
                    credential_id=new_org_credential.id,
                    modified_by="aaguirre@fluidattacks.com",
                    modified_date=datetime_utils.get_iso_date(),
                )
                await roots_model.update_root_state(
                    current_value=organization_root.state,
                    group_name=organization_root.group_name,
                    root_id=organization_root.id,
                    state=new_state,
                )
            if (
                isinstance(organization_root, GitRoot)
                and organization_root.id not in credential_roots
                and organization_root.state.credential_id
                == new_org_credential.id
            ):
                new_state = organization_root.state._replace(
                    credential_id=None,
                    modified_by="aaguirre@fluidattacks.com",
                    modified_date=datetime_utils.get_iso_date(),
                )
                await roots_model.update_root_state(
                    current_value=organization_root.state,
                    group_name=organization_root.group_name,
                    root_id=organization_root.id,
                    state=new_state,
                )


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
        await add_org_credential(
            loaders,
            organization_id,
            organization_name,
            credential_name,
            org_credentials,
        )
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
