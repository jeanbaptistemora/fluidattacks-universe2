# type: ignore

# pylint: disable=invalid-name,unexpected-keyword-arg,missing-kwoa
"""
Join the credentials with the same name in a group

Execution Time:    2022-06-06 at 21:01:04 UTC
Finalization Time: 2022-06-06 at 21:04:42 UTC
"""
from aioextensions import (
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.credentials import (
    get_credentials,
    remove,
    update_root_ids,
)
from db_model.credentials.types import (
    CredentialItem,
)
import logging
import logging.config
from organizations.domain import (
    get_all_active_group_names,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_credential(
    credential_name: str, credentials: tuple[CredentialItem, ...]
) -> None:
    duplicated_credentials: list[CredentialItem] = []
    for credential in credentials:
        if credential_name == credential.state.name:
            duplicated_credentials.append(credential)

    if len(duplicated_credentials) > 1:
        sorted_credentials = sorted(
            duplicated_credentials,
            key=lambda credential: len(credential.state.roots),
        )
        most_important_credential = sorted_credentials[-1]
        credential_roots = set()

        for credential in duplicated_credentials:
            credential_roots |= set(credential.state.roots)

        root_difference = credential_roots.difference(
            set(most_important_credential.state.roots)
        )
        if root_difference:
            await update_root_ids(
                current_value=most_important_credential.state,
                modified_by="aaguirre@fluidattacks.com",
                group_name=most_important_credential.group_name,
                credential_id=most_important_credential.id,
                root_ids=tuple(set(credential_roots)),
            )

        for credential in duplicated_credentials:
            if credential is not most_important_credential:
                await remove(
                    credential_id=credential.id,
                    group_name=credential.group_name,
                )


async def main() -> None:  # noqa: MC0001
    loaders = get_new_context()
    groups = sorted(await get_all_active_group_names(loaders=loaders))

    for index, group in enumerate(groups):
        print(group, index / len(groups))

        credentials: tuple[CredentialItem, ...] = await get_credentials(
            group_name=group
        )
        credentials_to_process = set()

        for credential in credentials:
            credentials_to_process.add(credential.state.name)

        for credential_name in credentials_to_process:
            await process_credential(credential_name, credentials)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
