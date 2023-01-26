# pylint: disable=invalid-name
# type: ignore
"""


Execution Time:
Finalization Time:
"""
from aioextensions import (
    run,
)
from batch_dispatch.utils.s3 import (
    download_repo,
)
import csv
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
    RootRequest,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from git import (
    Repo,
)
from git_self import (
    RebaseResult,
)
from organizations import (
    domain as orgs_domain,
)
import os
from tempfile import (
    TemporaryDirectory,
)
import time
from typing import (
    Optional,
    Tuple,
)
from unidiff import (
    Hunk,
    PatchedFile,
    PatchSet,
)


def rebase_one_commit_at_a_time(
    *,
    path: str,
    line: int,
    diff: PatchSet,
) -> Optional[Tuple[str, int]]:
    hunk: Hunk
    patch: PatchedFile

    if not diff:
        return None

    rebased_line = line
    for patch in diff:
        if patch.source_file == f"a/{path}":
            if patch.is_removed_file:
                # We cannot rebase something that was deleted
                return None
            # The original file matches the path to rebase
            # If the file was moved or something, this updates the path
            path = patch.source_file[2:]

            # Let's process the hunks to see what should be done with
            # the line numbers
            for hunk in patch:
                hunk_source_end = hunk.source_start + hunk.source_length - 1

                if line < hunk.source_start:
                    # The line exists before the hunk and therefore
                    # we do not need to modify the line
                    pass
                elif line > hunk_source_end:
                    # The line exists before this hunk and therefore
                    # we should increase/decrease the line number
                    rebased_line -= hunk.added - hunk.removed

    return (path, rebased_line)


def get_diffs(
    log: str, commit_prefix: str
) -> Tuple[Tuple[str, PatchSet], ...]:
    result: Tuple[Tuple[str, PatchSet], ...] = tuple()
    current_commit: Optional[str] = None
    lines: Tuple[str, ...] = tuple()
    for line in log.splitlines():
        if line.startswith(commit_prefix):
            if current_commit:
                result = (
                    *result,
                    (current_commit, PatchSet("\n".join(lines))),
                )
            current_commit = line.split(":")[-1]
            lines = tuple()
        else:
            lines = (*lines, line)
    if current_commit:
        result = (
            *result,
            (current_commit, PatchSet("\n".join(lines))),
        )
    return result


def rebase(
    repo: Repo,
    *,
    path: str,
    line: int,
    rev_a: str,
    rev_b: str,
) -> Optional[RebaseResult]:
    revs_str: str = repo.git.log(
        "--color=never",
        "--minimal",
        "--patch",
        "--unified=0",
        "--format=--COMMIT_HASH:%H",
        "--follow",
        "--reverse",
        "-p",
        f"{rev_a}...{rev_b}",
        "--",
        path,
    )

    # Let's rebase one commit at a time,
    # this way we reduce the probability of conflicts
    # and ensure line numbers are updated up to the latest possible commit
    for _, diff in get_diffs(revs_str, "--COMMIT_HASH"):
        if rebase_result := rebase_one_commit_at_a_time(
            path=path, line=line, diff=diff
        ):
            path, line = rebase_result
        else:
            # We cannot continue rebasing
            break

    return RebaseResult(path=path, line=line, rev=rev_a)


async def get_repos(roots: list[GitRoot], fusion_path: str) -> dict[str, Repo]:
    for root in roots:
        await download_repo(root.group_name, root, fusion_path)

    repos_dict = {
        root.id: Repo(os.path.join(fusion_path, root.state.nickname))
        for root in roots
    }

    for repo in repos_dict.values():
        repo.git.reset("--hard", "HEAD")

    return repos_dict


async def process_group(group: str, fusion_path: str) -> None:
    loaders: Dataloaders = get_new_context()

    findings: Tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group)
    vulns = await loaders.finding_vulnerabilities.load_many_chained(
        [fin.id for fin in findings]
    )
    vulns = tuple(
        vuln
        for vuln in vulns
        if vuln.type == VulnerabilityType.LINES
        and vuln.root_id
        and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
    )

    roots_dict: dict[str, GitRoot] = {
        root.id: root
        for root in (
            await loaders.root.load_many(
                [
                    RootRequest(group, vuln)
                    for vuln in {
                        vuln.root_id for vuln in vulns if vuln.root_id
                    }
                ]
            )
        )
        if root.state.status == RootStatus.ACTIVE
    }

    repos_dict = await get_repos(list(roots_dict.values()), fusion_path)

    vulns = tuple(
        vuln
        for vuln in vulns
        if vuln.root_id
        and vuln.root_id in roots_dict
        and roots_dict[vuln.root_id].state.status == RootStatus.ACTIVE
    )

    for vuln in vulns:
        if not vuln.root_id:
            continue
        repo = repos_dict[vuln.root_id]
        vulns_states = await loaders.vulnerability_historic_state.load(vuln.id)
        try:
            first_commit = repo.git.log(
                "--pretty=format:%H",
                "--follow",
                f'--until="{vulns_states[0].modified_date}"',
                "--",
                vuln.where,
            ).splitlines()[0]
        except IndexError:
            continue

        rev_b = "HEAD"
        if vuln.state.status == VulnerabilityStateStatus.SAFE:
            try:
                rev_b = repo.git.log(
                    "--pretty=format:%H",
                    "--follow",
                    f'--until="{vulns_states[-1].modified_date}"',
                    "--",
                    vuln.where,
                ).splitlines()[0]
            except IndexError:
                continue
        if rebase_result := rebase(
            repo,
            path=vuln.where,
            line=int(vuln.specific),
            rev_a=first_commit,
            rev_b=rev_b,
        ):
            with open("rebase.csv", "a+", encoding="utf-8") as handler:
                writer = csv.writer(handler)
                writer.writerow(
                    [
                        vuln.id,
                        (
                            f"{roots_dict[vuln.root_id].state.nickname}/"
                            f"{vuln.where}"
                        ),
                        vuln.state.status.value,
                        first_commit,
                        rev_b,
                        vuln.commit,
                        rebase_result.rev,
                        vuln.specific,
                        rebase_result.line,
                    ]
                )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    groups = sorted(
        await orgs_domain.get_all_active_group_names(loaders=loaders)
    )
    for group in reversed(groups):
        print(f"Processing group {group}")
        with TemporaryDirectory() as tmp:
            await process_group(group, tmp)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
