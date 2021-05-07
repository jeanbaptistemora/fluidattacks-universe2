# Standard libraries
import logging
import logging.config
from typing import (
    Any,
    List,
)

# Third party libraries
from aioextensions import (
    collect,
    schedule,
)

# Local libraries
from dataloaders import get_new_context
from groups.domain import get_group_digest_stats
from mailer import groups as groups_mail
from newutils import bugsnag as bugsnag_utils
from __init__ import (
    FI_MAIL_DIGEST,
    FI_TEST_PROJECTS_DIGEST,
)


bugsnag_utils.start_scheduler_session()

LOGGER = logging.getLogger(__name__)


async def sent_daily_digest(
    context: Any,
    group_name: str,
    mail_to: List[str],
) -> None:
    mail_context = await get_group_digest_stats(context, group_name)
    await schedule(groups_mail.send_mail_daily_digest(mail_to, mail_context))


async def main() -> None:
    """Daily Digest mail send to each analyst at the end of the day"""
    context = get_new_context()
    groups = FI_TEST_PROJECTS_DIGEST.split(',')
    mail_to = FI_MAIL_DIGEST.split(',')
    await collect([
        sent_daily_digest(context, group, mail_to)
        for group in groups
    ])
