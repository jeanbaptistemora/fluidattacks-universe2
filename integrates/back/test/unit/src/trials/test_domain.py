from datetime import (
    datetime,
)
from db_model.trials.enums import (
    TrialStatus,
)
from db_model.trials.types import (
    Trial,
)
from freezegun import (
    freeze_time,
)
import pytest
from trials.domain import (
    get_status,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["trial", "status"],
    [
        (
            Trial(
                email="",
                completed=False,
                start_date=None,
                extension_days=0,
                extension_date=None,
            ),
            TrialStatus.TRIAL,
        ),
        (
            Trial(
                email="",
                completed=False,
                extension_date=None,
                extension_days=0,
                start_date=datetime.fromisoformat("2021-12-20T00:00:00+00:00"),
            ),
            TrialStatus.TRIAL,
        ),
        (
            Trial(
                email="",
                completed=True,
                extension_date=None,
                extension_days=0,
                start_date=datetime.fromisoformat("2021-12-01T00:00:00+00:00"),
            ),
            TrialStatus.TRIAL_ENDED,
        ),
        (
            Trial(
                email="",
                completed=False,
                extension_date=datetime.fromisoformat(
                    "2021-12-30T00:00:00+00:00"
                ),
                extension_days=9,
                start_date=datetime.fromisoformat("2021-12-01T00:00:00+00:00"),
            ),
            TrialStatus.EXTENDED,
        ),
        (
            Trial(
                email="",
                completed=True,
                extension_date=datetime.fromisoformat(
                    "2021-12-01T00:00:00+00:00"
                ),
                extension_days=9,
                start_date=datetime.fromisoformat("2021-11-01T00:00:00+00:00"),
            ),
            TrialStatus.EXTENDED_ENDED,
        ),
    ],
)
@freeze_time("2022-01-01")
async def test_get_status(trial: Trial, status: TrialStatus) -> None:
    assert get_status(trial) == status
