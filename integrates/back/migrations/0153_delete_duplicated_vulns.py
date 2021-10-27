# pylint: disable=invalid-name
"""
This migration deletes duplicated vulnerabilities in all of the findings.
It uses the `vuln_type`, `where`, `specific` and `current_state` attributes
to determine if a vulnerability is a duplicate of another.

For each vulnerability:
    - If none of the duplicates has a treatment defined,
      the oldest vulnerability is kept and the rest are deleted.
    - If only one duplicate has treatment defined, that one is kept
      and the rest are deleted.
    - If multiple duplicates have treatment defined, the treatment is merged
      into the oldest duplicate and the rest are deleted.

Execution Time:
Finalization Time:
"""
from aioextensions import (
    collect,
    run,
)
from copy import (
    deepcopy,
)
from custom_types import (
    Vulnerability as VulnerabilityType,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.enums import (
    FindingStateJustification,
)
from functools import (
    partial,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    datetime as datetime_utils,
)
import time
from typing import (
    Dict,
    List,
)
from vulnerabilities import (
    dal as vulns_dal,
)
from vulnerabilities.domain import (
    utils as vulns_domain_utils,
)

DuplicatedVulnsIdx = Dict[int, Dict[int, Dict[int, List[int]]]]


async def _delete_vulnerability(vuln: VulnerabilityType) -> None:
    new_state = {
        "analyst": "acuberos@fluidattacks.com",
        "date": datetime_utils.get_now_as_str(),
        "justification": FindingStateJustification.DUPLICATED.value,
        "source": "asm",
        "state": "DELETED",
    }
    vuln["historic_state"].append(new_state)
    success = await vulns_dal.update(
        vuln["finding_id"],
        str(vuln["UUID"]),
        {"historic_state": vuln["historic_state"]},
    )
    if not success:
        print(f"[ERROR] Deleting vulnerability {vuln['UUID']} failed")


def _are_vulns_duplicates(
    vuln: VulnerabilityType, reference_vuln: VulnerabilityType
) -> bool:
    return (
        vuln["vuln_type"] == reference_vuln["vuln_type"]
        and vuln["where"] == reference_vuln["where"]
        and vuln["specific"] == reference_vuln["specific"]
        and vuln["current_state"] == reference_vuln["current_state"] == "open"
    )


def _remove_empty_keys(obj: DuplicatedVulnsIdx) -> DuplicatedVulnsIdx:
    _obj = deepcopy(obj)
    for key in obj.keys():
        for _key, _value in obj[key].items():
            if not _value:
                _obj[key].pop(_key)

    obj = deepcopy(_obj)
    for key, value in _obj.items():
        if not value:
            obj.pop(key)
    return obj


async def delete_duplicate_vulns_no_treatment(
    vulns: List[VulnerabilityType],
) -> None:
    sorted_vulns = sorted(
        vulns, key=lambda x: datetime_utils.get_from_str(x["report_date"])
    )
    vuln_ids_to_delete: str = "\n\t\t\t".join(
        [vuln["UUID"] for vuln in sorted_vulns[1:]]
    )
    print(
        "\t\tNo Treatment - Deleting:\n\t\t\t"
        f"{vuln_ids_to_delete} in favor of {sorted_vulns[0]['UUID']}"
    )
    await collect(_delete_vulnerability(vuln) for vuln in sorted_vulns[1:])


def get_duplicated_vulns_idx(
    findings_vulns: List[List[List[VulnerabilityType]]],
) -> DuplicatedVulnsIdx:
    duplicated_vulns: DuplicatedVulnsIdx = {}
    for group_idx, group_findings in enumerate(findings_vulns):
        duplicated_vulns.update({group_idx: {}})
        for finding_idx, finding_vulns in enumerate(group_findings):
            duplicated_vulns[group_idx].update({finding_idx: {}})
            for vuln_idx, vuln in enumerate(finding_vulns):
                if (
                    len(
                        list(
                            filter(
                                partial(
                                    _are_vulns_duplicates, reference_vuln=vuln
                                ),
                                finding_vulns,
                            )
                        )
                    )
                    > 1
                ):
                    vuln_key = vulns_domain_utils.get_hash_from_dict(vuln)
                    if vuln_key in duplicated_vulns[group_idx][finding_idx]:
                        duplicated_vulns[group_idx][finding_idx][
                            vuln_key
                        ].append(vuln_idx)
                    else:
                        duplicated_vulns[group_idx][finding_idx][vuln_key] = [
                            vuln_idx
                        ]
    return _remove_empty_keys(duplicated_vulns)


async def main() -> None:
    dataloaders = get_new_context()
    findings_loader = dataloaders.group_findings
    vulns_loader = dataloaders.finding_vulns
    groups = await groups_domain.get_active_groups()
    groups_findings = await findings_loader.load_many(groups)
    findings_vulns = list(
        await collect(
            vulns_loader.load_many([finding.id for finding in findings])
            for findings in groups_findings
        )
    )

    duplicated_vulns_idx = get_duplicated_vulns_idx(findings_vulns)
    for group_idx, findings in duplicated_vulns_idx.items():
        print(f"\nProcessing group {groups[group_idx]}...")
        for finding_idx, vulns in findings.items():
            print(
                "\tProcessing finding "
                f"{groups_findings[group_idx][finding_idx].title}..."
            )
            for vulns_idx in vulns.values():
                has_treatment = 0
                for vuln_idx in vulns_idx:
                    vuln = findings_vulns[group_idx][finding_idx][vuln_idx]
                    if len(vuln["historic_treatment"]) > 1:
                        has_treatment += 1
                if has_treatment == 0:
                    await delete_duplicate_vulns_no_treatment(
                        [
                            findings_vulns[group_idx][finding_idx][vuln_idx]
                            for vuln_idx in vulns_idx
                        ]
                    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
