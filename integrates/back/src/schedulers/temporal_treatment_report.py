from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
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
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def _days_to_end(date: datetime) -> int:
    return (date - datetime_utils.get_utc_now()).days


async def send_temporal_treatment_report() -> None:
    loaders: Dataloaders = get_new_context()
    groups_names = await orgs_domain.get_all_active_group_names(loaders)

    if FI_ENVIRONMENT == "production":
        groups_names = tuple(
            group
            for group in groups_names
            if group not in FI_TEST_PROJECTS.split(",")
        )

    group_findings: tuple[
        tuple[Finding, ...], ...
    ] = await loaders.group_findings.load_many(groups_names)

    if group_findings:
        for findings in group_findings:
            for finding in findings:
                locations: dict[str, Any] = {}
                vulns: tuple[
                    Vulnerability, ...
                ] = await loaders.finding_vulnerabilities_nzr.load(finding.id)
                for vuln in vulns:
                    if (
                        vuln.treatment
                        and vuln.treatment.status
                        == VulnerabilityTreatmentStatus.ACCEPTED
                        and (end_date := vuln.treatment.accepted_until)
                        and _days_to_end(end_date) in [7, 1]
                    ):
                        where: str = (vuln.state.where).split("/")[0]
                        locations[where] = {
                            "vuln_count": (
                                int(locations[where]["vuln_count"]) + 1
                                if locations.get(where)
                                else 1
                            )
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
        LOGGER.info("- temporary treatment report NOT sent")


async def main() -> None:
    await send_temporal_treatment_report()
