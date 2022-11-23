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
from newutils import (
    datetime as datetime_utils,
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
        "extension_date": datetime_utils.convert_from_iso_str(
            trial.extension_date
        )
        if trial.extension_date
        else "",
        "extension_days": trial.extension_days,
        "start_date": datetime_utils.convert_from_iso_str(trial.start_date)
        if trial.start_date
        else "",
        "state": enrollment_domain.get_enrollment_trial_state(trial),
    }
