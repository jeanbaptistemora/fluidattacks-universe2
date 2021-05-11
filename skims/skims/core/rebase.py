# Standard library

# Local libraries
from typing import AsyncIterator
from core.persist import (
    verify_permissions,
)
from integrates.dal import (
    get_finding_vulnerabilities,
    get_group_finding_ids,
)
from integrates.graphql import (
    create_session,
)
from model import (
    core_model,
)
from model.core_model import (
    Vulnerability,
)


async def iterate_vulnerabilities_to_rebase(
    group: str,
    namespace: str,
) -> AsyncIterator[Vulnerability]:
    for finding_id in await get_group_finding_ids(group):
        # Intentionally awaiting inside the loop in order to
        # allow integrates to rest a little, this query is heavy weighted
        store = await get_finding_vulnerabilities(
            # The finding code does not matter for our purpose, use any
            finding=core_model.FindingEnum.F008,
            finding_id=finding_id,
        )

        vulnerability: Vulnerability
        async for vulnerability in store.iterate():
            # The vulnerability must be for the namespace we are interested in
            # and have commit_hash.
            #
            # We'll allow skims to rebase all vulnerabilities,
            # not only the ones managed by skims.
            if (
                vulnerability.namespace == namespace
                and vulnerability.integrates_metadata
                and vulnerability.integrates_metadata.commit_hash
            ):
                yield vulnerability


async def main(
    group: str,
    namespace: str,
    token: str,
) -> bool:
    success: bool = True

    create_session(api_token=token)

    await verify_permissions(group=group)

    async for _ in iterate_vulnerabilities_to_rebase(
        group=group,
        namespace=namespace,
    ):
        pass

    return success
