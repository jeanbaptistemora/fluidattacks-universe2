# pylint: disable=invalid-name
"""
This migration aims to standarize the requirements field in several
finding's decription, taking their values from the criteria data.

Related issue:
https://gitlab.com/fluidattacks/product/-/issues/5229

Execution Time:    2021-08-25 at 09:22:15 UTC-05
Finalization Time: 2021-08-25 at 09:22:49 UTC-05
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
    Dict,
)
import yaml  # type: ignore

PROD: bool = True


def _get_requirements(
    vulns_data: Dict[str, Dict[str, str]],
    requirements_data: Dict[str, Dict[str, str]],
    finding_name: str,
    language: str,
) -> str:
    cve = finding_name[:3]
    requirements = [
        (
            f"{requ}. "
            f'{requirements_data[requ][language]["summary"]}'  # type: ignore
        )
        for requ in vulns_data[cve]["requirements"]
    ]
    return "".join(requirements)


async def process_finding(
    context: Dataloaders,
    vulns_data: Dict[str, Dict[str, str]],
    requirements_data: Dict[str, Dict[str, str]],
    group_name: str,
    finding_name: str,
) -> bool:
    # Get group language
    group_loader: DataLoader = context.group
    group: GroupType = await group_loader.load(group_name)
    language = group["language"]

    # Get finding id
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
        print(f"- ERROR finding {group_name} - {finding_name} NOT found")
        return False

    requirements = _get_requirements(
        vulns_data,
        requirements_data,
        finding_name,
        language,
    )

    success = False
    if PROD:
        success = await findings_dal.update(
            finding_id, {"requirements": requirements}
        )
    requ__to_print = requirements.replace("\n", ", ")
    print(
        f"- info: {group_name}, {language}, {finding_id}, "
        f'"{requ__to_print}", updated? {success}'
    )
    return success


async def main() -> None:
    # Read files with criteria
    with open(
        "../../../makes/makes/criteria/src/vulnerabilities/data.yaml", mode="r"
    ) as f:
        vulns_data = yaml.safe_load(f)

    with open(
        "../../../makes/makes/criteria/src/requirements/data.yaml", mode="r"
    ) as f:
        requirements_data = yaml.safe_load(f)

    # Read findings info
    with open("0120.csv", mode="r") as f:
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
    success = all(
        await collect(
            process_finding(
                context,
                vulns_data,
                requirements_data,
                finding["group_name"],
                finding["finding_name"],
            )
            for finding in info
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
