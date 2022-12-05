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
TRIAL_DAYS = 17


mail_upgrade_squad_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(groups_mail.send_upgrade_squad_notification)


async def send_upgrade_squad_notification() -> None:
    loaders: Dataloaders = get_new_context()

    stakeholders: tuple[
        Stakeholder, ...
    ] = await stakeholders_model.get_all_stakeholders()

    for stakeholder in stakeholders:
        enrollment: Enrollment = await loaders.enrollment.load(
            stakeholder.email
        )
        if (
            enrollment.enrolled
            and enrollment.trial.start_date
            and (
                datetime_utils.get_utc_now().date()
                - enrollment.trial.start_date.date()
            ).days
            == TRIAL_DAYS
        ):
            await mail_upgrade_squad_notification(loaders, stakeholder.email)


async def main() -> None:
    await send_upgrade_squad_notification()
