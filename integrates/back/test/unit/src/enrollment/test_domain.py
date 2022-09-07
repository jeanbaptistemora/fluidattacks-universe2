# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.enrollment.types import (
    Trial,
)
from enrollment.domain import (
    EnrollmentTrialState,
    get_enrollment_trial_state,
)
from freezegun import (  # type: ignore
    freeze_time,
)
import pytest

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["trial", "state"],
    [
        [
            Trial(
                completed=False,
                start_date="",
                extension_days=0,
                extension_date="",
            ),
            EnrollmentTrialState.TRIAL_ENDED,
        ],
        [
            Trial(
                completed=False,
                start_date="2021-12-20T00:00:00+00:00",
                extension_days=0,
                extension_date="",
            ),
            EnrollmentTrialState.TRIAL,
        ],
        [
            Trial(
                completed=True,
                start_date="2021-12-01T00:00:00+00:00",
                extension_days=0,
                extension_date="",
            ),
            EnrollmentTrialState.TRIAL_ENDED,
        ],
        [
            Trial(
                completed=True,
                start_date="2021-12-01T00:00:00+00:00",
                extension_days=9,
                extension_date="2021-12-30T00:00:00+00:00",
            ),
            EnrollmentTrialState.EXTENDED,
        ],
        [
            Trial(
                completed=True,
                start_date="2021-11-01T00:00:00+00:00",
                extension_days=9,
                extension_date="2021-12-01T00:00:00+00:00",
            ),
            EnrollmentTrialState.EXTENDED_ENDED,
        ],
    ],
)
@freeze_time("2022-01-01")
async def test_get_enrollment_trial_state(
    trial: Trial, state: EnrollmentTrialState
) -> None:
    assert get_enrollment_trial_state(trial) == state
