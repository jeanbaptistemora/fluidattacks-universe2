from datetime import (
    datetime,
)
from db_model import (
    companies as companies_model,
)
from db_model.companies.types import (
    CompanyMetadataToUpdate,
    Trial,
)
from newutils import (
    datetime as datetime_utils,
)

FREE_TRIAL_DAYS = 21


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
    domain: str,
    metadata: CompanyMetadataToUpdate,
) -> None:
    await companies_model.update_metadata(
        domain=domain,
        metadata=metadata,
    )
