# flake8: noqa
from dataloaders import (
    get_new_context,
)
from db_model.findings.enums import (
    FindingStatus,
)
from db_model.findings.types import (
    Finding,
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
)
from freezegun.api import (  # type: ignore
    freeze_time,
)
import pytest
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@freeze_time("2020-12-01")
async def test_update_unreliable_indicators_by_deps() -> None:
    loaders = get_new_context()
    finding_id = "422286126"
    vulnerability_id = "15375781-31f2-4953-ac77-f31134225747"
    await update_unreliable_indicators_by_deps(
        EntityDependency.upload_file,
        finding_ids=[finding_id],
        vulnerability_ids=[vulnerability_id],
    )
    finding: Finding = await loaders.finding.load(finding_id)
    expected_finding_output = FindingUnreliableIndicators(
        unreliable_closed_vulnerabilities=0,
        unreliable_is_verified=True,
        unreliable_open_vulnerabilities=1,
        unreliable_newest_vulnerability_report_date="2020-01-03T17:46:10+00:00",
        unreliable_oldest_open_vulnerability_report_date="2020-01-03T17:46:10+00:00",
        unreliable_oldest_vulnerability_report_date="2020-01-03T17:46:10+00:00",
        unreliable_status=FindingStatus.OPEN,
        unreliable_treatment_summary=FindingTreatmentSummary(
            accepted=0,
            accepted_undefined=0,
            in_progress=1,
            new=0,
        ),
        unreliable_where="test/data/lib_path/f060/csharp.cs",
    )
    assert finding.unreliable_indicators == expected_finding_output
