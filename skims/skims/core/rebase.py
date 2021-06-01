from core.persist import (
    verify_permissions,
)
import git
from integrates.dal import (
    do_update_vulnerability_commit,
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
import os
from typing import (
    AsyncIterator,
)
from utils.logs import (
    log,
    log_exception,
)
from utils.repositories import (
    get_repo,
    rebase,
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
    repository: str,
    token: str,
) -> bool:
    success: bool = True

    create_session(api_token=token)

    await verify_permissions(group=group)

    repo = get_repo(repository, search_parent_directories=False)

    async for vulnerability in iterate_vulnerabilities_to_rebase(
        group=group,
        namespace=namespace,
    ):
        try:
            if rebase_data := rebase(
                repo,
                path=vulnerability.what,
                line=int(vulnerability.where),
                rev_a=vulnerability.integrates_metadata.commit_hash,
                rev_b="HEAD",
            ):
                await log(
                    "info",
                    (
                        "Vulnerability will be rebased from:\n"
                        "  from path: %s\n"
                        "    line: %s\n"
                        "    commit: %s\n"
                        "  to path:   %s:\n"
                        "    line: %s\n"
                        "    commit: %s\n"
                    ),
                    vulnerability.what,
                    vulnerability.where,
                    vulnerability.integrates_metadata.commit_hash,
                    rebase_data.path,
                    rebase_data.line,
                    rebase_data.rev,
                )
                if not await do_update_vulnerability_commit(
                    vuln_commit=rebase_data.rev,
                    vuln_id=vulnerability.integrates_metadata.uuid,
                    vuln_what=os.path.join(namespace, rebase_data.path),
                    vuln_where=str(rebase_data.line),
                ):
                    success = False
        except git.GitError as exc:
            await log_exception("error", exc)

    return success
