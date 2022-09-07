# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .common import (
    scheduler_send_mail,
)
from aioextensions import (
    collect,
)
from context import (
    BASE_URL,
    FI_MAIL_PROJECTS,
)
from custom_exceptions import (
    StakeholderNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Notification,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from findings import (
    domain as findings_domain,
)
from itertools import (
    chain,
)
import logging
import logging.config
from mailer import (
    findings as findings_mail,
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


async def get_remediated_findings() -> None:
    """Summary mail send with findings that have not been verified yet."""
    loaders: Dataloaders = get_new_context()
    active_groups = await orgs_domain.get_all_active_group_names(loaders)
    findings = tuple(
        chain.from_iterable(
            await collect(
                findings_domain.get_pending_verification_findings(
                    loaders, group
                )
                for group in active_groups
            )
        )
    )

    if not findings:
        return

    try:
        mail_to = [FI_MAIL_PROJECTS]
        mail_context_findings: list[dict[str, str]] = [
            {
                "finding_name": finding.title,
                "finding_url": (
                    f"{BASE_URL}/groups/{finding.group_name}/"
                    f"{finding.id}/description"
                ),
                "group": finding.group_name,
            }
            for finding in findings
        ]
        mail_context: dict[str, Any] = {
            "findings": mail_context_findings,
            "total": len(findings),
        }
        stakeholders: tuple[
            Stakeholder, ...
        ] = await loaders.stakeholder.load_many(mail_to)
        stakeholders_email = [
            stakeholder.email
            for stakeholder in stakeholders
            if Notification.REMEDIATE_FINDING
            in stakeholder.notifications_preferences.email
        ]
        scheduler_send_mail(
            loaders,
            findings_mail.send_mail_new_remediated,
            stakeholders_email,
            mail_context,
        )
    except (TypeError, KeyError, StakeholderNotFound) as ex:
        LOGGER.exception(ex, extra={"extra": locals()})


async def main() -> None:
    await get_remediated_findings()
