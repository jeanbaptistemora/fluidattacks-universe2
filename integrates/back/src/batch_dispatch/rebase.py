from aioextensions import (
    collect,
)
from batch.dal import (
    delete_action,
)
from batch.types import (
    BatchProcessing,
)
from batch_dispatch.utils.s3 import (
    download_repo,
)
from concurrent.futures import (
    ThreadPoolExecutor,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    InvalidVulnerabilityAlreadyExists,
    LineDoesNotExistInTheLinesOfCodeRange,
    VulnerabilityPathDoesNotExistInToeLines,
    VulnerabilityUrlFieldDoNotExistInToeInputs,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from git.cmd import (
    Git,
)
from git.exc import (
    GitError,
)
from git.repo.base import (
    Repo,
)
import json
import logging
import logging.config
from newutils import (
    git_self as git_utils,
)
from newutils.vulnerabilities import (
    get_advisories,
    ignore_advisories,
)
import os
from roots import (
    domain as roots_domain,
)
from settings import (
    LOGGING,
)
import tempfile
from typing import (
    Any,
    Optional,
    Tuple,
)
from vulnerabilities.domain.rebase import (
    rebase as rebase_vulnerability,
)
from vulnerabilities.domain.snippet import (
    generate_snippet,
    set_snippet,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _get_vulnerabilities_to_rebase(
    loaders: Dataloaders,
    group_name: str,
    git_root: GitRoot,
) -> tuple[Vulnerability, ...]:
    findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    findings_vulns: tuple[
        tuple[Vulnerability, ...], ...
    ] = await loaders.finding_vulnerabilities.load_many(
        tuple(find.id for find in findings)
    )
    vulnerabilities: tuple[Vulnerability, ...] = tuple(
        vuln
        for vulns in findings_vulns
        for vuln in vulns
        if vuln.root_id == git_root.id
        and vuln.state.commit is not None
        and vuln.type == VulnerabilityType.LINES
        and vuln.state.status == VulnerabilityStateStatus.OPEN
    )
    return vulnerabilities


def _rebase_vulnerability(
    repo: Repo,
    vulnerability: Vulnerability,
    states: Tuple[VulnerabilityState, ...],
) -> Optional[git_utils.RebaseResult]:
    try:
        if (
            states[0].commit
            and states[0].commit != "0000000000000000000000000000000000000000"
            and (
                result := git_utils.rebase(
                    repo,
                    path=ignore_advisories(states[0].where),
                    line=int(states[0].specific),
                    rev_a=states[0].commit,
                    rev_b="HEAD",
                )
            )
        ):
            return result
    except GitError as exc:
        LOGGER.error(
            "Failed to rebase vulnerability",
            extra=dict(extra={"vuln_id": vulnerability.id, "exception": exc}),
        )
    return None


async def _rebase_vulnerability_integrates(
    *,
    loaders: Any,
    finding_id: str,
    finding_vulns_data: Tuple[Vulnerability, ...],
    vulnerability_commit: str,
    vulnerability_id: str,
    vulnerability_where: str,
    vulnerability_specific: str,
    vulnerability_type: VulnerabilityType,
) -> None:
    local_vars = locals()
    with suppress(
        InvalidVulnerabilityAlreadyExists,
    ):
        try:
            await rebase_vulnerability(
                loaders=loaders,
                finding_id=finding_id,
                finding_vulns_data=finding_vulns_data,
                vulnerability_commit=vulnerability_commit,
                vulnerability_id=vulnerability_id,
                vulnerability_where=vulnerability_where,
                vulnerability_specific=vulnerability_specific,
                vulnerability_type=vulnerability_type,
            )
        except (
            VulnerabilityPathDoesNotExistInToeLines,
            LineDoesNotExistInTheLinesOfCodeRange,
            VulnerabilityUrlFieldDoNotExistInToeInputs,
        ) as exception:
            local_vars.pop("loaders", None)
            local_vars.pop("finding_vulns_data", None)
            LOGGER.error(
                "Failed to rebase vulnerability in integrates",
                extra=dict(extra={"exception": exception, **local_vars}),
            )


async def rebase_root(
    loaders: Dataloaders, group_name: str, repo: Repo, git_root: GitRoot
) -> None:
    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await _get_vulnerabilities_to_rebase(loaders, group_name, git_root)
    vulns_states: Tuple[
        Tuple[VulnerabilityState, ...], ...
    ] = await loaders.vulnerability_historic_state.load_many(
        [vuln.id for vuln in vulnerabilities]
    )
    with ThreadPoolExecutor(max_workers=8) as executor:
        all_rebase: tuple[
            tuple[Optional[git_utils.RebaseResult], Vulnerability], ...
        ] = tuple(
            executor.map(
                lambda vuln: (
                    _rebase_vulnerability(repo, vuln[0], vuln[1]),
                    vuln[0],
                ),
                zip(vulnerabilities, vulns_states),
            )
        )
    await collect(
        [
            _rebase_vulnerability_integrates(
                loaders=loaders,
                finding_id=vuln.finding_id,
                finding_vulns_data=tuple(
                    item
                    for item in vulnerabilities
                    if item.finding_id == vuln.finding_id
                ),
                vulnerability_commit=rebase_result.rev,
                vulnerability_id=vuln.id,
                vulnerability_where=vuln.state.where
                if get_advisories(vuln.state.where)
                else rebase_result.path,
                vulnerability_specific=str(rebase_result.line),
                vulnerability_type=vuln.type,
            )
            for rebase_result, vuln in all_rebase
            if rebase_result
            and (
                rebase_result.path != vuln.state.where
                or str(rebase_result.line) != vuln.state.specific
            )
        ]
    )
    loaders.vulnerability.clear_all()
    vulnerabilities = await loaders.vulnerability.load_many(
        [vuln.id for vuln in vulnerabilities]
    )
    futures = []
    for vuln in vulnerabilities:
        if (not vuln.state.snippet) and (
            snippet := generate_snippet(vuln.state, repo)
        ):
            futures.append(set_snippet(vuln, vuln.state, snippet))
    await collect(futures, workers=50)


async def rebase(*, item: BatchProcessing) -> None:
    group_name: str = item.entity
    try:
        root_nicknames = json.loads(item.additional_info)["roots"]
    except json.JSONDecodeError:
        root_nicknames = item.additional_info.split(",")

    dataloaders: Dataloaders = get_new_context()
    group_roots_loader = dataloaders.group_roots
    group_roots: Tuple[GitRoot, ...] = tuple(
        root
        for root in await group_roots_loader.load(group_name)
        if root.state.status == RootStatus.ACTIVE
    )
    # In the off case there are multiple roots with the same nickname
    if item.additional_info == "*":
        root_ids = tuple(root.id for root in group_roots)
    else:
        root_ids = tuple(
            roots_domain.get_root_id_by_nickname(
                nickname=nickname,
                group_roots=group_roots,
                only_git_roots=True,
            )
            for nickname in root_nicknames
        )

    roots: Tuple[GitRoot, ...] = tuple(
        root for root in group_roots if root.id in root_ids
    )

    for git_root in roots:
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            repo_path = f"{tmpdir}/{git_root.state.nickname}"
            Git().execute(
                [
                    "git",
                    "config",
                    "--global",
                    "--add",
                    "safe.directory",
                    repo_path,
                ]
            )
            downloaded = await download_repo(group_name, git_root, tmpdir)
            if downloaded:
                repo = Repo(
                    repo_path,
                    search_parent_directories=True,
                )
                repo.git.reset("--hard", "HEAD")
                os.chdir(repo_path)
                await rebase_root(dataloaders, group_name, repo, git_root)
                await delete_action(
                    action_name=item.action_name,
                    additional_info=item.additional_info,
                    entity=item.entity,
                    subject=item.subject,
                    time=item.time,
                )
