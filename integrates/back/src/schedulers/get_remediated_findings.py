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
from custom_types import (
    MailContent as MailContentType,
)
from dataloaders import (
    get_new_context,
)
from findings import (
    domain as findings_domain,
)
from groups import (
    domain as groups_domain,
)
from itertools import (
    chain,
)
import logging
import logging.config
from mailer import (
    findings as findings_mail,
)
from settings import (
    LOGGING,
)
from typing import (
    cast,
    Dict,
    List,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def get_remediated_findings() -> None:
    """Summary mail send with findings that have not been verified yet"""
    active_groups = await groups_domain.get_active_groups()
    findings = tuple(
        chain.from_iterable(
            await collect(
                findings_domain.get_pending_verification_findings(
                    get_new_context(), group
                )
                for group in active_groups
            )
        )
    )

    if findings:
        try:
            mail_to = [FI_MAIL_PROJECTS]
            mail_context: MailContentType = {"findings": [], "total": 0}
            for finding in findings:
                cast(List[Dict[str, str]], mail_context["findings"]).append(
                    {
                        "finding_name": finding.title,
                        "finding_url": (
                            f"{BASE_URL}/groups/{finding.group_name}/"
                            f"{finding.id}/description"
                        ),
                        "group": finding.group_name,
                    }
                )
            mail_context["total"] = len(findings)
            scheduler_send_mail(
                findings_mail.send_mail_new_remediated, mail_to, mail_context
            )
        except (TypeError, KeyError) as ex:
            LOGGER.exception(ex, extra={"extra": locals()})


async def main() -> None:
    await get_remediated_findings()
