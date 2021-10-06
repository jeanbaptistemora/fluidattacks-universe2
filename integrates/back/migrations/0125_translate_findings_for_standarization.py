# pylint: disable=invalid-name
"""
This migration aims to fix the language for several drafts created in
previous migrations, in the scope of the findings type standarization effort.

If the findings' group is in Spanish, the related text fields will be updated.

Related issue:
https://gitlab.com/fluidattacks/product/-/issues/4903

Execution Time:    2021-08-23 at 22:15:49 UTC-05
Finalization Time: 2021-08-23 at 22:16:00 UTC-05
"""

from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    run,
)
import csv
from custom_types import (
    Group as GroupType,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from findings import (
    dal as findings_dal,
)
import time
from typing import (
    Any,
    Dict,
)
import yaml  # type: ignore

PROD: bool = True


def _validate_not_empty(field: str) -> str:
    if field != "__empty__":
        return field.strip()
    return ""


def _get_finding_type_data_es(data: Any, finding_name: str) -> Dict[str, str]:
    cve = finding_name[:3]
    criteria = data[cve]

    finding_data = {
        "attack_vector_desc": _validate_not_empty(criteria["es"]["impact"]),
        "effect_solution": _validate_not_empty(
            criteria["es"]["recommendation"]
        ),
        "threat": _validate_not_empty(criteria["es"]["threat"]),
        "vulnerability": _validate_not_empty(criteria["es"]["description"]),
    }
    return finding_data


async def process_finding(
    data: Any,
    info: Dict[str, str],
) -> bool:
    if info["language"] == "en":
        print(
            f'   --- WARNING finding {info["group_name"]} - '
            f'{info["finding_name"]} NOT processed'
        )
        return True
    type_data_es = _get_finding_type_data_es(data, info["finding_name"])

    success = False
    if PROD:
        success = await findings_dal.update(info["finding_id"], type_data_es)
    print(
        f'   --- finding {info["group_name"]} - '
        f'{info["finding_name"]} updated: {success}'
    )
    return success


async def _expand_info(
    context: Dataloaders,
    group_name: str,
    finding_name: str,
) -> Dict[str, str]:
    group_loader: DataLoader = context.group
    group: GroupType = await group_loader.load(group_name)

    group_findings_loader: DataLoader = context.group_findings
    group_findings = await group_findings_loader.load(group_name)
    group_findings_titles = [finding["title"] for finding in group_findings]
    finding_id = ""
    if finding_name in group_findings_titles:
        finding_id = next(
            finding["id"]
            for finding in group_findings
            if finding["title"] == finding_name
        )
    else:
        print(f"   --- ERROR finding {group_name} - {finding_name} NOT found")
    return {
        "group_name": group_name,
        "language": group.get("language"),
        "finding_name": finding_name,
        "finding_id": finding_id,
    }


async def main() -> None:
    # Read file with criteria
    with open(
        "../../../makes/makes/criteria/src/vulnerabilities/data.yaml",
        mode="r",
        encoding="utf8",
    ) as data_yaml:
        criteria_data = yaml.safe_load(data_yaml)

    # Read findings info
    with open("0125.csv", mode="r") as f:  # noqa
        reader = csv.reader(f)
        info = [
            {
                "group_name": row[0],
                "finding_name": row[1],
            }
            for row in reader
            if "group" not in row[0]
        ]

    context: Dataloaders = get_new_context()
    expanded_info = await collect(
        _expand_info(
            context,
            finding["group_name"],
            finding["finding_name"],
        )
        for finding in info
    )
    print(f"   === to_process ({len(expanded_info)}): {expanded_info[:3]}")

    success = all(
        await collect(
            [
                process_finding(criteria_data, finding)
                for finding in expanded_info
            ]
        )
    )

    print(f"   === success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
