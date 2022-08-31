from db_model.enrollment.types import (
    Enrollment,
    Trial,
)
from enum import (
    Enum,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


class EnrollmentTrialState(str, Enum):
    EXTENDED: str = "EXTENDED"
    EXTENDED_ENDED: str = "EXTENDED_ENDED"
    TRIAL: str = "TRIAL"
    TRIAL_ENDED: str = "TRIAL_ENDED"


def _get_enrollment_trial_state(trial: Trial) -> str:
    if not trial.extension_date:
        return EnrollmentTrialState.TRIAL_ENDED.value

    return EnrollmentTrialState.TRIAL.value


async def resolve(
    parent: Enrollment,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> dict[str, Any]:
    trial: Trial = parent.trial

    return {
        "completed": trial.completed,
        "extension_date": trial.extension_date,
        "extension_days": trial.extension_days,
        "start_date": trial.start_date,
        "state": _get_enrollment_trial_state(trial),
    }
