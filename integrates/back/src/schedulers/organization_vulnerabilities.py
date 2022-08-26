from aioextensions import (
    collect,
)
import csv
from custom_exceptions import (
    UnsanitizedInputFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from findings.domain.core import (
    get_severity_score,
)
from itertools import (
    chain,
)
from newutils.datetime import (
    get_as_str,
    get_now,
)
from newutils.validations import (
    validate_sanitized_csv_input,
)
from organizations.domain import (
    iterate_organizations_and_groups,
)
import os
from reports.it_report import (
    ITReport,
)
import tempfile


async def get_findings(
    *, group_name: str, loaders: Dataloaders
) -> tuple[Finding, ...]:
    return await loaders.group_findings.load(group_name)


def format_data(value: str) -> str:
    try:
        validate_sanitized_csv_input(str(value))
        return value
    except UnsanitizedInputFound:
        return ""


async def get_data(
    *, groups: tuple[str, ...], loaders: Dataloaders, organization_name: str
) -> list[list[str]]:
    organization_findings: tuple[tuple[Finding, ...], ...] = await collect(
        tuple(
            get_findings(group_name=group_name, loaders=loaders)
            for group_name in groups
        ),
        workers=4,
    )
    findings_ord = tuple(
        sorted(
            chain.from_iterable(organization_findings),
            key=lambda finding: get_severity_score(finding.severity),
            reverse=True,
        )
    )
    report = ITReport(
        data=findings_ord,
        group_name=organization_name,
        loaders=loaders,
        treatments=set(VulnerabilityTreatmentStatus),
        states=set(
            [
                VulnerabilityStateStatus["CLOSED"],
                VulnerabilityStateStatus["OPEN"],
            ]
        ),
        verifications=set(),
        closing_date=None,
        finding_title="",
        age=None,
        min_severity=None,
        max_severity=None,
        last_report=None,
        min_release_date=None,
        max_release_date=None,
        generate_raw_data=False,
    )
    await report.generate_data()

    return report.raw_data


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    async for _, org_name, org_groups in (
        iterate_organizations_and_groups(loaders)
    ):
        date: str = get_as_str(get_now(), date_format="%Y-%m-%dT%H-%M-%S")
        rows: list[list[str]] = await get_data(
            groups=org_groups, loaders=loaders, organization_name=org_name
        )
        with tempfile.TemporaryDirectory() as directory:
            with open(
                os.path.join(directory, f"{org_name}-{date}.csv"),
                "w",
                encoding="utf-8",
            ) as csv_file:
                writer = csv.writer(
                    csv_file,
                    delimiter=",",
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL,
                )
                writer.writerow(rows[0])
                writer.writerows(
                    [[format_data(value) for value in row] for row in rows[1:]]
                )
