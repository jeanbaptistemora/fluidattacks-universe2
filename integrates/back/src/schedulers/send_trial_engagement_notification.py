from aioextensions import (
    collect,
)
from custom_exceptions import (
    UnableToSendMail,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.companies.types import (
    Company,
)
from db_model.groups.enums import (
    GroupManaged,
)
from decorators import (
    retry_on_exceptions,
)
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer import (
    analytics as analytics_mail,
    groups as groups_mail,
)
from mailer.types import (
    TrialEngagementInfo,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Awaitable,
    Callable,
    Optional,
)

mail_add_stakeholders_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(groups_mail.send_add_stakeholders_notification)

mail_send_define_treatments_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(groups_mail.send_define_treatments_notification)

mail_send_add_repositories_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(groups_mail.send_add_repositories_notification)

mail_support_channels_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(groups_mail.send_support_channels_notification)

mail_analytics_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(analytics_mail.send_trial_analytics_notification)

mail_upgrade_squad_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(groups_mail.send_upgrade_squad_notification)


async def send_trial_engagement_notification() -> None:
    notifications: dict[
        int, Callable[[Dataloaders, TrialEngagementInfo], Awaitable[None]]
    ] = {
        3: mail_add_stakeholders_notification,
        5: mail_send_define_treatments_notification,
        7: mail_send_add_repositories_notification,
        9: mail_support_channels_notification,
        11: mail_analytics_notification,
        17: mail_upgrade_squad_notification,
    }
    loaders = get_new_context()
    groups = await orgs_domain.get_all_active_groups(loaders)
    domains = tuple(group.created_by.split("@")[1] for group in groups)
    companies: tuple[Optional[Company], ...] = await loaders.company.load_many(
        domains
    )

    await collect(
        tuple(
            notification(
                loaders,
                TrialEngagementInfo(
                    email_to=group.created_by,
                    group_name=group.name,
                ),
            )
            for group, company in zip(groups, companies)
            if group.state.managed == GroupManaged.TRIAL
            and company
            and company.trial.start_date
            and (
                notification := notifications.get(
                    datetime_utils.get_days_since(company.trial.start_date)
                )
            )
        )
    )


async def main() -> None:
    await send_trial_engagement_notification()
