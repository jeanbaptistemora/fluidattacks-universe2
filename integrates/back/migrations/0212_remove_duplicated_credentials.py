# type: ignore

# pylint: disable=invalid-name,unexpected-keyword-arg,missing-kwoa
"""
Remove duplicated credentials in groups

Execution Time:    2022-05-09 at 16:48:35 UTCUTC
Finalization Time: 2022-05-09 at 16:54:51 UTCUTC
"""
from aioextensions import (
    collect,
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
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def get_creds_ids(
    credentials: tuple[CredentialItem, ...], group: Any
) -> list[str]:
    remove_creds_ids = []
    for cred_a in credentials:
        if cred_a.id in remove_creds_ids:
            continue

        roots_for_a = cred_a.state.roots
        for cred_b in credentials:
            if (
                cred_a.metadata.type != cred_b.metadata.type
                or cred_a.id == cred_b.id
                or len(
                    set(cred_a.state.roots).intersection(
                        set(cred_b.state.roots)
                    )
                )
                > 0
            ):
                continue
            if (
                (  # pylint: disable=too-many-boolean-expressions
                    cred_a.state.key is not None
                    and cred_a.state.key == cred_b.state.key
                )
                or (
                    cred_a.state.token is None
                    and cred_a.state.token == cred_b.state.token
                )
                or (
                    (
                        cred_a.state.user is None
                        and cred_a.state.user == cred_b.state.user
                    )
                    and (
                        cred_a.state.password is None
                        and cred_a.state.password == cred_b.state.password
                    )
                )
            ):
                roots_for_a = {*roots_for_a, *cred_b.state.roots}
                remove_creds_ids = [*remove_creds_ids, cred_b.id]
        if (
            len(cred_a.state.roots) != len(roots_for_a)
            and len(roots_for_a) > 1
        ):
            try:
                await update_root_ids(
                    current_value=cred_a.state,
                    modified_by="drestrepo@fluiidattacks.com",
                    group_name=group,
                    credential_id=cred_a.id,
                    root_ids=tuple(roots_for_a),
                )
            except Exception:  # pylint: disable=broad-except
                LOGGER.error(
                    "failed to dupdate root ids",
                    extra={"extra": {"group": group}},
                )


async def main() -> None:  # noqa: MC0001
    loaders = get_new_context()
    groups = sorted(await get_all_active_group_names(loaders=loaders))

    for group in groups:
        credentials: tuple[CredentialItem, ...] = await get_credentials(
            group_name=group
        )
        if not credentials:
            continue

        remove_creds_ids = await get_creds_ids(credentials, group)

        await collect(
            [
                remove(credential_id=cred_id, group_name=group)
                for cred_id in remove_creds_ids
            ]
        )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
