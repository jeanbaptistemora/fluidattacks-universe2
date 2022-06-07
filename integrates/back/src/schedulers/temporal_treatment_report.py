from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import logging
from mailer import (
    vulnerabilities as vulns_mail,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def days_to_end(date: str) -> int:
    days = (
        datetime_utils.get_datetime_from_iso_str(date)
        - datetime_utils.get_now()
    ).days
    return days


async def send_temporal_treatment_report() -> None:
    loaders: Dataloaders = get_new_context()
    groups_names = await orgs_domain.get_all_active_group_names(loaders)

    if FI_ENVIRONMENT == "production":
        groups_names = tuple(
            group
            for group in groups_names
            if group not in FI_TEST_PROJECTS.split(",")
        )

    group_findings: Tuple[
        Tuple[Finding, ...], ...
    ] = await loaders.group_findings.load_many(groups_names)

    if group_findings:
        for findings in group_findings:
            for finding in findings:
                locations: dict[str, Any] = {}
                vulns: Tuple[
                    Vulnerability, ...
                ] = await loaders.finding_vulnerabilities_nzr.load(finding.id)
                for vuln in vulns:
                    if (
                        vuln.treatment
                        and vuln.treatment.status
                        == VulnerabilityTreatmentStatus.ACCEPTED
                        and (end_date := vuln.treatment.accepted_until)
                        and days_to_end(end_date) in [7, 1]
                    ):
                        locations[vuln.where] = {
                            "accepted_until": (
                                datetime_utils.get_date_from_iso_str(end_date)
                            ),
                            "days_left": days_to_end(end_date),
                        }
                if locations:
                    await vulns_mail.send_mail_temporal_treatment_report(
                        loaders=loaders,
                        finding_id=finding.id,
                        finding_title=finding.title,
                        group_name=finding.group_name,
                        locations=locations,
                    )

    else:
        LOGGER.info("- temporal treatment report NOT sent")
        return


async def main() -> None:
    await send_temporal_treatment_report()
