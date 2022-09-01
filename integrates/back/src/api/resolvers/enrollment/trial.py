from db_model.enrollment.types import (
    Enrollment,
    Trial,
)
from enrollment import (
    domain as enrollment_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


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
        "state": enrollment_domain.get_enrollment_trial_state(trial),
    }
