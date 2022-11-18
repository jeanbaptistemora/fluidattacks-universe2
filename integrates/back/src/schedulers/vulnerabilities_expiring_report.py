# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
from context import (
    FI_ENVIRONMENT,
    FI_MAIL_COS,
    FI_MAIL_CTO,
    FI_TEST_PROJECTS,
)
from custom_exceptions import (
    UnableToSendMail,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Notification,
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
from decorators import (
    retry_on_exceptions,
)
from group_access import (
    domain as group_access_domain,
)
import logging
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer import (
    groups as groups_mail,
)
from mailer.utils import (
    get_organization_name,
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
from stakeholders.domain import (
    is_fluid_staff,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
    TypedDict,
)

logging.config.dictConfig(LOGGING)

# Constants
DAYS_TO_EXPIRING = 7
LOGGER = logging.getLogger(__name__)

mail_vulnerabilities_expiring = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=3,
    sleep_seconds=2,
)(groups_mail.send_mail_vulnerabilities_expiring)


class ExpiringDataType(TypedDict):
    org_name: str
    email_to: Tuple[str, ...]
    group_expiring_findings: Dict[str, Dict[str, int]]


def days_to_end(date: str) -> int:
    days = (
        datetime_utils.get_datetime_from_iso_str(date)
        - datetime_utils.get_now()
    ).days
    return days


async def expiring_vulnerabilities(
    loaders: Dataloaders, finding_id: str
) -> Dict[str, int]:
    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load(finding_id)
    return {
        f"{vulnerability.state.where}"
        + f"({vulnerability.state.specific})": days_to_end(
            vulnerability.treatment.accepted_until
        )
        for vulnerability in vulnerabilities
        if vulnerability.treatment
        and vulnerability.treatment.status
        == VulnerabilityTreatmentStatus.ACCEPTED
        and (end_date := vulnerability.treatment.accepted_until)
        and days_to_end(end_date) in range(7)
    }


async def findings_close_to_expiring(
    loaders: Dataloaders, group_name: str
) -> Dict[str, Dict[str, int]]:
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )

    finding_types = (finding.title for finding in findings)

    vulnerabilities = await collect(
        [expiring_vulnerabilities(loaders, finding.id) for finding in findings]
    )

    findings_to_expiring = dict(zip(finding_types, vulnerabilities))
    return {
        finding_type: data
        for (finding_type, data) in findings_to_expiring.items()
        if data
    }


def unique_emails(
    expiring_data: Dict[str, ExpiringDataType],
    email_list: Tuple[str, ...],
) -> Tuple[str, ...]:
    if expiring_data:
        email_list += expiring_data.popitem()[1]["email_to"]
        unique_emails(expiring_data, email_list)

    return tuple(set(email_list))


async def get_fluid_stakeholders(
    loaders: Dataloaders, group_name: str, notification: str, roles: set[str]
) -> List[str]:
    stakeholders = (
        await group_access_domain.get_stakeholders_email_by_preferences(
            loaders=loaders,
            group_name=group_name,
            notification=notification,
            roles=roles,
        )
    )
    return [
        stakeholder
        for stakeholder in stakeholders
        if is_fluid_staff(stakeholder)
    ]


async def send_temporal_treatment_report() -> None:
    loaders: Dataloaders = get_new_context()
    groups_names = await orgs_domain.get_all_active_group_names(loaders)

    if FI_ENVIRONMENT == "production":
        groups_names = tuple(
            group
            for group in groups_names
            if group not in FI_TEST_PROJECTS.split(",")
        )

    groups_org_names = await collect(
        [
            get_organization_name(loaders, group_name)
            for group_name in groups_names
        ]
    )

    roles: set[str] = {
        "resourcer",
        "customer_manager",
        "user_manager",
        "vulnerability_manager",
    }

    groups_stakeholders_email: Tuple[List[str], ...] = await collect(
        [
            get_fluid_stakeholders(
                loaders=loaders,
                group_name=group_name,
                notification=Notification.UPDATED_TREATMENT,
                roles=roles,
            )
            for group_name in groups_names
        ]
    )

    groups_expiring_findings = await collect(
        [
            findings_close_to_expiring(loaders, group_name)
            for group_name in groups_names
        ]
    )

    groups_data: Dict[str, ExpiringDataType] = dict(
        zip(
            groups_names,
            [
                ExpiringDataType(
                    org_name=org_name,
                    email_to=tuple(email_to),
                    group_expiring_findings=expiring_findings,
                )
                for org_name, email_to, expiring_findings in zip(
                    groups_org_names,
                    groups_stakeholders_email,
                    groups_expiring_findings,
                )
            ],
        )
    )

    groups_data = {
        group_name: data
        for (group_name, data) in groups_data.items()
        if data["email_to"] and data["group_expiring_findings"]
    }

    for email in unique_emails(dict(groups_data), ()):
        user_content: Dict[str, Any] = {
            "groups_data": {
                group_name: {
                    "org_name": data["org_name"],
                    "group_expiring_findings": data["group_expiring_findings"],
                }
                for group_name, data in groups_data.items()
                if email in data["email_to"]
            }
        }

        try:
            await mail_vulnerabilities_expiring(
                loaders=loaders,
                context=user_content,
                email_to=email,
                email_cc=[FI_MAIL_COS, FI_MAIL_CTO],
            )
            LOGGER.info(
                "Temporal treatment alert email sent",
                extra={"extra": {"email": email}},
            )
        except KeyError:
            LOGGER.info(
                "Key error, Temporal treatment alert email not sent",
                extra={"extra": {"email": email}},
            )
            continue
    LOGGER.info("Temporal treatment alert execution finished.")
    LOGGER.info("Finding expiring report data: %s", groups_data)


async def main() -> None:
    await send_temporal_treatment_report()