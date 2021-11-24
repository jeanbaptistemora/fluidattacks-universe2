from aioextensions import (
    collect,
)
from concurrent.futures import (
    ThreadPoolExecutor,
)
from core.persist import (
    verify_permissions,
)
import git
from git.repo.base import (
    Repo,
)
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
    Optional,
)
from utils.logs import (
    log,
    log_blocking,
    log_exception_blocking,
)
from utils.repositories import (
    get_repo,
    rebase,
    RebaseResult,
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
                # Exception: WF(AsyncIterator is subtype of iterator)
                yield vulnerability  # NOSONAR


def _rebase(
    repo: Repo, vulnerability: Vulnerability
) -> Optional[RebaseResult]:
    try:
        if result := rebase(
            repo,
            path=vulnerability.what,
            line=int(vulnerability.where),
            rev_a=vulnerability.integrates_metadata.commit_hash,
            rev_b="HEAD",
        ):
            log_blocking(
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
                result.path,
                result.line,
                result.rev,
            )
            return result
    except git.GitError as exc:
        log_exception_blocking("error", exc)
    return None


async def main(
    group: str,
    namespace: str,
    repository: str,
    token: str,
) -> bool:
    create_session(api_token=token)

    await verify_permissions(group=group)

    repo = get_repo(repository, search_parent_directories=False)

    vulnerabilities = [
        vulnerability
        async for vulnerability in iterate_vulnerabilities_to_rebase(
            group=group,
            namespace=namespace,
        )
    ]
    with ThreadPoolExecutor(max_workers=4) as executor:
        all_rebase = list(
            executor.map(
                lambda vuln: (_rebase(repo, vuln), vuln), vulnerabilities
            )
        )
    futures = [
        do_update_vulnerability_commit(
            vuln_commit=rebase_data.rev,
            vuln_id=vulnerability.integrates_metadata.uuid,
            vuln_what=os.path.join(namespace, rebase_data.path),
            vuln_where=str(rebase_data.line),
        )
        for rebase_data, vulnerability in all_rebase
        if rebase_data
    ]
    await log("info", "Updating vulnerability commits")
    return all(await collect(futures))
