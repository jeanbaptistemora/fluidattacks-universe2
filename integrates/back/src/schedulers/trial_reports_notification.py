# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
TRIAL_DAYS = 15


mail_trial_reports_notification = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(groups_mail.send_trial_reports_notification)


async def send_trial_reports_notification() -> None:
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
            await mail_trial_reports_notification(
                loaders, stakeholder.email, groups_name[0]
            )


async def main() -> None:
    await send_trial_reports_notification()
