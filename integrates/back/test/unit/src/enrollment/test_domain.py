from datetime import (
    datetime,
)
from db_model.companies.types import (
    Trial,
)
from db_model.enrollment.enums import (
    EnrollmentTrialState,
)
from enrollment.domain import (
    get_enrollment_trial_state,
)
from freezegun import (
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
        (
            Trial(
                completed=False,
                start_date=None,
                extension_days=0,
                extension_date=None,
            ),
            EnrollmentTrialState.TRIAL_ENDED,
        ),
        (
            Trial(
                completed=False,
                extension_date=None,
                extension_days=0,
                start_date=datetime.fromisoformat("2021-12-20T00:00:00+00:00"),
            ),
            EnrollmentTrialState.TRIAL,
        ),
        (
            Trial(
                completed=True,
                extension_date=None,
                extension_days=0,
                start_date=datetime.fromisoformat("2021-12-01T00:00:00+00:00"),
            ),
            EnrollmentTrialState.TRIAL_ENDED,
        ),
        (
            Trial(
                completed=True,
                extension_date=datetime.fromisoformat(
                    "2021-12-30T00:00:00+00:00"
                ),
                extension_days=9,
                start_date=datetime.fromisoformat("2021-12-01T00:00:00+00:00"),
            ),
            EnrollmentTrialState.EXTENDED,
        ),
        (
            Trial(
                completed=True,
                extension_date=datetime.fromisoformat(
                    "2021-12-01T00:00:00+00:00"
                ),
                extension_days=9,
                start_date=datetime.fromisoformat("2021-11-01T00:00:00+00:00"),
            ),
            EnrollmentTrialState.EXTENDED_ENDED,
        ),
    ],
)
@freeze_time("2022-01-01")
async def test_get_enrollment_trial_state(
    trial: Trial, state: EnrollmentTrialState
) -> None:
    assert get_enrollment_trial_state(trial) == state
