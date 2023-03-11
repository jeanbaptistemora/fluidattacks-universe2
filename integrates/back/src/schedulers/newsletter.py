from aioextensions import (
    collect,
)
from context import (
    FI_ENVIRONMENT,
    FI_MAIL_CUSTOMER_EXPERIENCE,
    FI_TEST_PROJECTS,
)
from custom_exceptions import (
    UnableToSendMail,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from decorators import (
    retry_on_exceptions,
)
import logging
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer.common import (
    send_mail_newsletter,
)
from mailer.utils import (
    get_group_emails_by_notification,
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

mail_newsletter = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=3,
    sleep_seconds=2,
)(send_mail_newsletter)


def unique_emails(
    groups_data: dict[str, Tuple[str, ...]],
    email_list: tuple[str, ...],
) -> tuple[str, ...]:
    if groups_data:
        email_list += groups_data.popitem()[1]
        return unique_emails(groups_data, email_list)

    return tuple(set(email_list))


async def send_newsletter() -> None:
    loaders: Dataloaders = get_new_context()
    groups_names = await orgs_domain.get_all_active_group_names(loaders)

    if FI_ENVIRONMENT == "production":
        groups_names = [
            group
            for group in groups_names
            if group not in FI_TEST_PROJECTS.split(",")
        ]

    groups_stakeholders_email: tuple[list[str], ...] = await collect(
        [
            get_group_emails_by_notification(
                loaders=loaders,
                group_name=group_name,
                notification="newsletter",
            )
            for group_name in groups_names
        ]
    )

    groups_data: dict[str, Tuple[str, ...]] = dict(
        zip(
            groups_names,
            [tuple(email_to) for email_to in groups_stakeholders_email],
        )
    )

    groups_data = {
        group_name: stakeholders_email
        for (group_name, stakeholders_email) in groups_data.items()
        if stakeholders_email
    }

    LOGGER.info(
        "Newsletter recipients",
        extra={
            "extra": {
                "GroupsData": groups_data,
                "UniqueEmails": unique_emails(dict(groups_data), ()),
            }
        },
    )

    for email in FI_MAIL_CUSTOMER_EXPERIENCE.split(","):
        try:
            await mail_newsletter(
                loaders=loaders,
                context={},
                email_to=email,
                email_cc=[],
            )
            LOGGER.info(
                "Newsletter email sent",
                extra={"extra": {"email": email}},
            )
        except KeyError:
            LOGGER.info(
                "Key error, newsletter email not sent",
                extra={"extra": {"email": email}},
            )
            continue
    LOGGER.info("Newsletter scheduler execution finished.")


async def main() -> None:
    await send_newsletter()
