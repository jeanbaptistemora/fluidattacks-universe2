from aioextensions import (
    collect,
)
from botocore.exceptions import (
    ClientError,
)
from context import (
    CI_COMMIT_REF_NAME,
    FI_AWS_S3_ANALYTICS_BUCKET,
)
import csv
from custom_exceptions import (
    UnavailabilityError,
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
import logging
import logging.config
from newutils.datetime import (
    get_as_str,
    get_now,
)
from organizations.domain import (
    get_all_active_group_names,
    iterate_organizations_and_groups,
    update_url,
)
import os
from reports.it_report import (
    ITReport,
)
from s3.operations import (
    sign_url,
)
from s3.resource import (
    get_s3_resource,
)
from settings.logger import (
    LOGGING,
)
import tempfile

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
TTL = 21600


async def upload_file(bucket: str, file_path: str, file_name: str) -> None:
    with open(file_path, mode="rb") as file_object:
        client = await get_s3_resource()
        try:
            await client.upload_fileobj(
                file_object,
                bucket,
                file_name.lstrip("/"),
            )
        except ClientError as ex:
            LOGGER.exception(ex, extra={"extra": locals()})
            raise UnavailabilityError() from ex


async def get_findings(
    *, group_name: str, loaders: Dataloaders
) -> tuple[Finding, ...]:
    return await loaders.group_findings.load(group_name)


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
    folder_date: str = get_as_str(get_now(), date_format="%Y-%m-%d")
    all_group_names: set[str] = set(await get_all_active_group_names(loaders))
    async for org_id, org_name, org_groups in (
        iterate_organizations_and_groups(loaders)
    ):
        date: str = get_as_str(get_now(), date_format="%Y-%m-%dT%H-%M-%S")
        rows: list[list[str]] = await get_data(
            groups=tuple(all_group_names.intersection(org_groups)),
            loaders=loaders,
            organization_name=org_name,
        )
        with tempfile.TemporaryDirectory() as directory:
            with open(
                os.path.join(directory, f"{org_id}-{date}.csv"),
                mode="w",
                encoding="utf-8",
            ) as csv_file:
                writer = csv.writer(
                    csv_file,
                    delimiter=",",
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL,
                )
                writer.writerow(rows[0])
                writer.writerows(rows[1:])

            filename: str = (
                f"{CI_COMMIT_REF_NAME}/reports/organizations"
                f"/{folder_date}/{org_id}-{date}.csv"
            )
            await upload_file(
                FI_AWS_S3_ANALYTICS_BUCKET,
                csv_file.name,
                filename,
            )
            signed_url: str = await sign_url(
                filename, TTL, FI_AWS_S3_ANALYTICS_BUCKET
            )
            await update_url(
                org_id,
                org_name,
                signed_url,
            )
