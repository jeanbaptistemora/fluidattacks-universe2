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
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Notification,
)
from db_model.users.types import (
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

    if findings:
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
            users: tuple[Stakeholder, ...] = await loaders.user.load_many(
                mail_to
            )
            users_email = [
                user.email
                for user in users
                if Notification.REMEDIATE_FINDING
                in user.notifications_preferences.email
            ]
            scheduler_send_mail(
                findings_mail.send_mail_new_remediated,
                users_email,
                mail_context,
            )
        except (TypeError, KeyError) as ex:
            LOGGER.exception(ex, extra={"extra": locals()})


async def main() -> None:
    await get_remediated_findings()
