from custom_exceptions import (
    UnableToSendMail,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.enrollment.types import (
    Enrollment,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from decorators import (
    retry_on_exceptions,
)
from group_access import (
    domain as group_access_domain,
)
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer import (
    groups as groups_mail,
)
from newutils import (
    datetime as datetime_utils,
)

# Constants
TRIAL_DAYS = 7


mail_send_add_repositories_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(groups_mail.send_add_repositories_notification)


async def send_add_repositories_notification() -> None:
    loaders: Dataloaders = get_new_context()

    stakeholders: tuple[
        Stakeholder, ...
    ] = await stakeholders_model.get_all_stakeholders()

    for stakeholder in stakeholders:
        enrollment: Enrollment = await loaders.enrollment.load(
            stakeholder.email
        )

        groups_name = await group_access_domain.get_stakeholder_groups_names(
            loaders, stakeholder.email, True
        )

        if (
            enrollment.enrolled
            and enrollment.trial.start_date
            and (
                datetime_utils.get_now().date()
                - datetime_utils.get_date_from_iso_str(
                    enrollment.trial.start_date
                )
            ).days
            == TRIAL_DAYS
        ):
            await mail_send_add_repositories_notification(
                loaders, stakeholder.email, groups_name[0]
            )


async def main() -> None:
    await send_add_repositories_notification()
