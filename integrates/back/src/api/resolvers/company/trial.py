# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.companies.types import (
    Company,
    Trial,
)
from enrollment.domain import (
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
        "extension_date": trial.extension_date,
        "extension_days": trial.extension_days,
        "start_date": trial.start_date,
        "state": _get_state(trial),
    }
