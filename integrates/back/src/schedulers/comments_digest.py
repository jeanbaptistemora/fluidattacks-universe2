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
from db_model.findings.types import (
    Finding,
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


async def send_comment_digest() -> None:
    loaders: Dataloaders = get_new_context()
    groups_names = await orgs_domain.get_all_active_group_names(loaders)
    group_stakeholders_email = await collect(
        [
            group_access_domain.get_group_stakeholders_emails(
                loaders,
                group_name,
            )
            for group_name in groups_names
        ]
    )

    if FI_ENVIRONMENT == "development":
        groups_names = tuple(
            group
            for group in groups_names
            if group not in FI_TEST_PROJECTS.split(",")
        )

    group_findings: Tuple[
        Tuple[Finding, ...], ...
    ] = await loaders.group_findings.load_many(groups_names)

    email_data = dict(
        zip(
            groups_names,
            [
                {
                    "email_to": group_emails,
                    "group_comments": [],
                    "event_comments": [],
                    "finding_comments": [
                        finding.title for finding in findings
                    ],
                }
                for group_emails, findings in zip(
                    group_stakeholders_email, group_findings
                )
            ],
        )
    )
    LOGGER.info("- Email data to notify: %s", email_data)


async def main() -> None:
    await send_comment_digest()
