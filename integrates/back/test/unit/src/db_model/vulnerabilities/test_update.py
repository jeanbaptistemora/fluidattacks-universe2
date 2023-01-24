from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_mocked_path,
    set_mocks_return_values,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities import (
    update_historic_entry,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
)
from decimal import (
    Decimal,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["vulnerability", "entry"],
    [
        [
            Vulnerability(
                created_by="unittest@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2019-09-12T13:45:48+00:00"
                ),
                finding_id="463461507",
                group_name="unittesting",
                hacker_email="unittest@fluidattacks.com",
                id="e248e8e0-0323-41c7-bc02-4ee61d09f9c4",
                state=VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    source=Source.ASM,
                    specific="7777",
                    status=VulnerabilityStateStatus.VULNERABLE,
                    where="192.168.1.18",
                    commit=None,
                    reasons=None,
                    other_reason=None,
                    tool=None,
                    snippet=None,
                ),
                type=VulnerabilityType.LINES,
                bug_tracking_system_url=None,
                custom_severity=None,
                developer=None,
                event_id=None,
                hash=None,
                root_id=None,
                skims_method=None,
                skims_technique=None,
                stream=None,
                tags=None,
                treatment=VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat(
                        "2019-09-13T13:45:48+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                    acceptance_status=None,
                    accepted_until=datetime.fromisoformat(
                        "2021-01-16T17:46:10+00:00"
                    ),
                    justification="accepted justification",
                    assigned="integratesuser@gmail.com",
                    modified_by="integratesuser@gmail.com",
                ),
                unreliable_indicators=VulnerabilityUnreliableIndicators(
                    unreliable_closing_date=None,
                    unreliable_source=Source.ASM,
                    unreliable_efficacy=Decimal("0"),
                    unreliable_last_reattack_date=None,
                    unreliable_last_reattack_requester=None,
                    unreliable_last_requested_reattack_date=None,
                    unreliable_reattack_cycles=0,
                    unreliable_treatment_changes=2,
                ),
                verification=None,
                zero_risk=None,
            ),
            VulnerabilityState(
                commit=None,
                modified_by="unittest@fluidattacks.com",
                modified_date=datetime.fromisoformat(
                    "2022-01-24T17:46:10+00:00"
                ),
                source=Source.ASM,
                specific="7777",
                status=VulnerabilityStateStatus.SAFE,
                where="192.168.1.18",
            ),
        ]
    ],
)
@patch(get_mocked_path("operations.put_item"), new_callable=AsyncMock)
@patch(get_mocked_path("operations.update_item"), new_callable=AsyncMock)
async def test_update_historic_entry(
    mock_operations_update_item: AsyncMock,
    mock_operations_put_item: AsyncMock,
    entry: VulnerabilityState,
    vulnerability: Vulnerability,
) -> None:
    mocked_objects = [mock_operations_update_item, mock_operations_put_item]
    mocked_paths = ["operations.update_item", "operations.put_item"]
    mocks_args = [
        [vulnerability.finding_id, vulnerability.id, entry],
        [vulnerability.id, entry],
    ]
    assert set_mocks_return_values(
        mocked_objects=mocked_objects,
        paths_list=mocked_paths,
        mocks_args=mocks_args,
    )
    await update_historic_entry(
        current_value=vulnerability,
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability.id,
        entry=entry,
    )
    assert all(mock_object.called is True for mock_object in mocked_objects)
