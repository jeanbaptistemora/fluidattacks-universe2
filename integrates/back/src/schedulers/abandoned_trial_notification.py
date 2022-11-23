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
INACTIVE_HOURS = [1, 24]


mail_abandoned_trial_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(groups_mail.send_abandoned_trial_notification)


async def send_abandoned_trial_notification() -> None:
    loaders: Dataloaders = get_new_context()

    stakeholders: tuple[
        Stakeholder, ...
    ] = await stakeholders_model.get_all_stakeholders()

    for stakeholder in stakeholders:
        enrollment: Enrollment = await loaders.enrollment.load(
            stakeholder.email
        )
        if (
            not enrollment.enrolled
            and stakeholder.registration_date
            and (
                delta_hours := (
                    datetime_utils.get_now()
                    - datetime_utils.get_datetime_from_iso_str(
                        stakeholder.registration_date
                    )
                ).total_seconds()
                // 3600
            )
            and delta_hours in INACTIVE_HOURS
        ):
            await mail_abandoned_trial_notification(
                loaders, stakeholder.email, delta_hours == 1
            )


async def main() -> None:
    await send_abandoned_trial_notification()
