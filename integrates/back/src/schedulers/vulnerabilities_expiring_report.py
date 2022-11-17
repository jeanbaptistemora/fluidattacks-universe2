# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
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
from db_model.stakeholders.types import (
    Stakeholder,
)
from group_access import (
    domain as group_access_domain,
)
import logging
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
    Tuple,
    TypedDict,
)

logging.config.dictConfig(LOGGING)

# Constants
DAYS_TO_EXPIRING = 7
LOGGER = logging.getLogger(__name__)


class ExpiringDataType(TypedDict):
    email_to: Tuple[str, ...]
    group_expiring_findings: Tuple[Finding, ...]


def days_to_end(date: str) -> int:
    days = (
        datetime_utils.get_datetime_from_iso_str(date)
        - datetime_utils.get_now()
    ).days
    return days


async def findings_close_to_expiring(
    loaders: Dataloaders, group_name: str
) -> Tuple[Finding, ...]:
    findings_to_expiring: Tuple[
        Finding, ...
    ] = await loaders.group_findings.load(group_name)
    return findings_to_expiring


async def send_temporal_treatment_report() -> None:
    loaders: Dataloaders = get_new_context()
    groups_names = await orgs_domain.get_all_active_group_names(loaders)

    if FI_ENVIRONMENT == "production":
        groups_names = tuple(
            group
            for group in groups_names
            if group not in FI_TEST_PROJECTS.split(",")
        )

    groups_stakeholders: Tuple[Tuple[Stakeholder, ...], ...] = await collect(
        [
            group_access_domain.get_group_stakeholders(
                loaders,
                group_name,
            )
            for group_name in groups_names
        ]
    )

    groups_stakeholders_email: Tuple[Tuple[str, ...], ...] = tuple(
        tuple(
            stakeholder.email
            for stakeholder in group_stakeholders
            if Notification.NEW_COMMENT
            in stakeholder.state.notifications_preferences.email
        )
        for group_stakeholders in groups_stakeholders
    )

    groups_expiring_findings: Tuple[Tuple[Finding, ...], ...] = await collect(
        [
            findings_close_to_expiring(loaders, group_name)
            for group_name in groups_names
        ]
    )

    data = tuple(
        zip(
            groups_names,
            groups_stakeholders_email,
            groups_expiring_findings,
        )
    )

    LOGGER.info("Finding expiring report data: %s", data)


async def main() -> None:
    await send_temporal_treatment_report()
