# pylint: disable=invalid-name
"""
Deletes all duplicate vulnerabilities reported by Machine in SCA findings,
giving priority to those that have treatment
and reopening them in case they were incorrectly closed

Execution Time:    2022-11-12 at 03:34:26 UTC
Finalization Time: 2022-11-12 at 04:11:39 UTC
"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
    VulnerabilityState,
)
from newutils.datetime import (  # type: ignore
    get_datetime_from_iso_str,
    get_utc_now,
)
from organizations.domain import (
    get_all_active_group_names,
)
import re
import time
from unreliable_indicators.enums import (
    EntityAttr,
)
from unreliable_indicators.operations import (
    update_finding_unreliable_indicators,
)
from vulnerabilities.domain import (
    remove_vulnerability,
    update_metadata_and_state,
)

SCA_REGEX = (
    r"^(?P<where>.*)\s+\((?P<package_name>.*)\s+"
    r"v(?P<package_version>.*)\)\s+\[(?P<advisories>.*)\]$"
)


def get_duplicate_vulns(
    vulns: list[Vulnerability],
) -> dict[tuple[str, ...], list[Vulnerability]]:
    original_items: dict[tuple[str, ...], Vulnerability] = {}
    duplicate_items: dict[tuple[str, ...], list[Vulnerability]] = {}
    for vuln in vulns:
        if match := re.match(SCA_REGEX, vuln.state.where):
            match_dict = match.groupdict()
            item: tuple[str, ...] = (
                vuln.root_id or "",
                match_dict["where"],
                match_dict["package_name"],
                match_dict["package_version"],
                vuln.state.specific,
                vuln.type.value,
            )
            if item not in original_items:
                original_items.update({item: vuln})
                continue

            if item not in duplicate_items:
                duplicate_items.update({item: [original_items[item], vuln]})
            else:
                duplicate_items[item].append(vuln)

    return duplicate_items


def process_duplicates(
    duplicates: dict[tuple[str, ...], list[Vulnerability]]
) -> tuple[list[Vulnerability], list[Vulnerability]]:
    vulns_to_delete: list[Vulnerability] = []
    vulns_to_open: list[Vulnerability] = []
    for vulns in duplicates.values():
        treatment_vulns: list[Vulnerability] = []
        no_treatment_vulns: list[Vulnerability] = []
        has_open_vulns: bool = False
        for vuln in vulns:
            (
                treatment_vulns
                if vuln.treatment is not None
                else no_treatment_vulns
            ).append(vuln)
            if (
                not has_open_vulns
                and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
            ):
                has_open_vulns = True

        original_vuln: Vulnerability
        if len(treatment_vulns) == 0:
            original_vuln = no_treatment_vulns[0]
            vulns_to_delete.extend(no_treatment_vulns[1:])
        else:
            vulns_to_delete.extend(no_treatment_vulns)
            treatment_sorted_vulns = sorted(
                treatment_vulns,
                key=lambda x: (
                    -(
                        x.treatment is not None
                        and x.treatment.acceptance_status is not None
                    ),
                    get_datetime_from_iso_str(
                        x.treatment.modified_date
                        if x.treatment is not None
                        else "2000-01-01T00:00:00+00:00"
                    ),
                ),
            )
            original_vuln = treatment_sorted_vulns[0]
            if len(treatment_sorted_vulns) > 1:
                vulns_to_delete.extend(treatment_sorted_vulns[1:])

        if (
            original_vuln.state.status == VulnerabilityStateStatus.SAFE
            and has_open_vulns
        ):
            vulns_to_open.append(original_vuln)

    return vulns_to_delete, vulns_to_open


async def main() -> None:
    loaders = get_new_context()
    groups = await get_all_active_group_names(loaders)
    groups_findings = (
        await loaders.group_drafts_and_findings.load_many_chained(list(groups))
    )
    sca_findings: list[Finding] = [
        finding
        for finding in groups_findings
        if finding.state.status
        not in [FindingStateStatus.DELETED, FindingStateStatus.MASKED]
        and any(finding.title.startswith(code) for code in ["011", "393"])
    ]
    sca_vulns = await loaders.finding_vulnerabilities_released_nzr.load_many(
        [finding.id for finding in sca_findings]
    )
    num_findings: int = len(sca_findings)
    for idx, (finding, vulns) in enumerate(zip(sca_findings, sca_vulns)):
        print(
            f"Processing finding {finding.title} "
            f"in group {finding.group_name}({idx+1}/{num_findings})..."
        )
        machine_vulns: list[Vulnerability] = sorted(
            [
                vuln
                for vuln in vulns
                if vuln.state.source == Source.MACHINE
                or vuln.hacker_email == "machine@fluidattacks.com"
            ],
            key=lambda x: x.created_date,
        )
        duplicate_vulns = get_duplicate_vulns(machine_vulns)

        if duplicate_vulns:
            vulns_to_delete, vulns_to_open = process_duplicates(
                duplicate_vulns
            )
            print("\t" + f"Deleting {len(vulns_to_delete)} vulnerabilities...")
            await collect(
                (
                    remove_vulnerability(
                        loaders,
                        finding.id,
                        vuln.id,
                        VulnerabilityStateReason.DUPLICATED,
                        "acuberos@fluidattacks.com",
                        True,
                    )
                    for vuln in vulns_to_delete
                ),
                workers=15,
            )
            await collect(
                (
                    update_metadata_and_state(
                        vulnerability=vuln,
                        new_metadata=VulnerabilityMetadataToUpdate(),
                        new_state=VulnerabilityState(
                            modified_by="acuberos@fluidattacks.com",
                            modified_date=get_utc_now(),
                            source=Source.MACHINE,
                            specific=vuln.state.specific,
                            status=VulnerabilityStateStatus.VULNERABLE,
                            where=vuln.state.where,
                            commit=vuln.state.commit,
                            justification=(
                                vuln.state.justification  # type: ignore
                            ),
                            tool=vuln.state.tool,
                            snippet=vuln.state.snippet,
                        ),
                    )
                    for vuln in vulns_to_open
                ),
                workers=15,
            )
            await update_finding_unreliable_indicators(
                finding.id,
                {
                    EntityAttr.closed_vulnerabilities,
                    EntityAttr.newest_vulnerability_report_date,
                    EntityAttr.oldest_open_vulnerability_report_date,
                    EntityAttr.oldest_vulnerability_report_date,
                    EntityAttr.open_vulnerabilities,
                    EntityAttr.status,
                    EntityAttr.where,
                    EntityAttr.treatment_summary,
                    EntityAttr.verification_summary,
                },
            )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
