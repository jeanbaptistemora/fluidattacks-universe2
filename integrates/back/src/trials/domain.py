from dataloaders import (
    Dataloaders,
)
from db_model import (
    trials as trials_model,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.trials.enums import (
    TrialStatus,
)
from db_model.trials.types import (
    Trial,
    TrialMetadataToUpdate,
)
from newutils import (
    datetime as datetime_utils,
)

FREE_TRIAL_DAYS = 21


def get_status(trial: Trial) -> TrialStatus:
    if trial.extension_date:
        if trial.completed:
            return TrialStatus.EXTENDED_ENDED
        return TrialStatus.EXTENDED

    if trial.completed:
        return TrialStatus.TRIAL_ENDED
    return TrialStatus.TRIAL


def get_remaining_days(trial: Trial) -> int:
    days = 0

    if trial.extension_date:
        days = trial.extension_days - datetime_utils.get_days_since(
            trial.extension_date
        )
    elif trial.start_date:
        days = FREE_TRIAL_DAYS - datetime_utils.get_days_since(
            trial.start_date
        )

    return max(0, days)


def has_expired(trial: Trial) -> bool:
    return (
        not trial.completed
        and trial.start_date is not None
        and get_remaining_days(trial) == 0
    )


async def update_metadata(
    email: str,
    metadata: TrialMetadataToUpdate,
) -> None:
    await trials_model.update_metadata(
        email=email,
        metadata=metadata,
    )


async def in_trial(
    loaders: Dataloaders, user_email: str, organization: Organization
) -> bool:
    trial = await loaders.trial.load(user_email)
    completed = trial and trial.completed

    if completed or organization.payment_methods:
        return False
    return True
