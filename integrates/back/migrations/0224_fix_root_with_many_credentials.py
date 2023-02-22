# type: ignore

# pylint: disable=invalid-name,unexpected-keyword-arg,missing-kwoa
"""
Remove root from credential if that root has a new credential

Execution Time:    2022-06-06 at 19:31:54 UTC
Finalization Time: 2022-06-06 at 20:20:09 UTC
"""
from aioextensions import (
    run,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
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


async def process_root(root_id: str, group_name: str) -> None:
    credentials: tuple[CredentialItem, ...] = await get_credentials(
        group_name=group_name
    )
    root_credentials: list[CredentialItem] = []
    for credential in credentials:
        if root_id in credential.state.roots:
            root_credentials.append(credential)

    if len(root_credentials) > 1:
        sorted_credentials = sorted(
            root_credentials,
            key=lambda credential: datetime.fromisoformat(
                credential.state.modified_date
            ),
        )
        last_credential = sorted_credentials[-1]

        for credential in root_credentials:
            if credential is not last_credential:
                credential_roots = [*credential.state.roots]
                credential_roots.remove(root_id)
                await update_root_ids(
                    current_value=credential.state,
                    modified_by="aaguirre@fluidattacks.com",
                    group_name=credential.group_name,
                    credential_id=credential.id,
                    root_ids=tuple(set(credential_roots)),
                )
                if not credential_roots:
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
        roots_to_process = set()

        for credential in credentials:
            roots_to_process |= set(credential.state.roots)

        for root_id in roots_to_process:
            await process_root(root_id, group)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
