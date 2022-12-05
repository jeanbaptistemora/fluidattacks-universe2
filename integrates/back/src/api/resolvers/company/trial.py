from db_model.companies.types import (
    Company,
    Trial,
)
from db_model.enrollment.enums import (
    EnrollmentTrialState,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


def _get_state(trial: Trial) -> EnrollmentTrialState:
    if trial.extension_date:
        if trial.completed:
            return EnrollmentTrialState.EXTENDED_ENDED
        return EnrollmentTrialState.EXTENDED

    if trial.completed:
        return EnrollmentTrialState.TRIAL_ENDED
    return EnrollmentTrialState.TRIAL


def resolve(
    parent: Company,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> dict[str, Any]:
    trial = parent.trial

    return {
        "completed": trial.completed,
        "extension_date": trial.extension_date or "",
        "extension_days": trial.extension_days,
        "start_date": trial.start_date or "",
        "state": _get_state(trial),
    }
