from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    FindingState,
)
from db_model.utils import (
    adjust_historic_dates,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_adjust_historic_dates() -> None:
    historic = (
        FindingState(
            modified_by="",
            modified_date=datetime.fromisoformat("2021-12-12T00:00:01+00:00"),
            source=Source.ASM,
            status=FindingStateStatus.CREATED,
        ),
        FindingState(
            modified_by="",
            modified_date=datetime.fromisoformat("2021-12-12T00:00:01+00:00"),
            source=Source.ASM,
            status=FindingStateStatus.SUBMITTED,
        ),
        FindingState(
            modified_by="",
            modified_date=datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
            source=Source.ASM,
            status=FindingStateStatus.REJECTED,
        ),
        FindingState(
            modified_by="",
            modified_date=datetime.fromisoformat("2021-01-01T00:00:00+00:00"),
            source=Source.ASM,
            status=FindingStateStatus.SUBMITTED,
        ),
        FindingState(
            modified_by="",
            modified_date=datetime.fromisoformat("2021-12-30T14:35:01+00:00"),
            source=Source.ASM,
            status=FindingStateStatus.APPROVED,
        ),
    )
    assert adjust_historic_dates(historic) == (
        FindingState(
            modified_by="",
            modified_date=datetime.fromisoformat("2021-12-12T00:00:01+00:00"),
            source=Source.ASM,
            status=FindingStateStatus.CREATED,
        ),
        FindingState(
            modified_by="",
            modified_date=datetime.fromisoformat("2021-12-12T00:00:02+00:00"),
            source=Source.ASM,
            status=FindingStateStatus.SUBMITTED,
        ),
        FindingState(
            modified_by="",
            modified_date=datetime.fromisoformat("2021-12-12T00:00:03+00:00"),
            source=Source.ASM,
            status=FindingStateStatus.REJECTED,
        ),
        FindingState(
            modified_by="",
            modified_date=datetime.fromisoformat("2021-12-12T00:00:04+00:00"),
            source=Source.ASM,
            status=FindingStateStatus.SUBMITTED,
        ),
        FindingState(
            modified_by="",
            modified_date=datetime.fromisoformat("2021-12-30T14:35:01+00:00"),
            source=Source.ASM,
            status=FindingStateStatus.APPROVED,
        ),
    )
