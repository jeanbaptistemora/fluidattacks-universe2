from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_mocked_path,
    set_mocks_return_values,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityToolImpact,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTool,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
    VulnerabilityZeroRisk,
)
from decimal import (
    Decimal,
)
from freezegun import (
    freeze_time,
)
from newutils.datetime import (
    get_now_minus_delta,
)
import pytest
from typing import (
    Union,
)
from unittest.mock import (
    AsyncMock,
    patch,
)
from vulnerabilities.domain import (
    get_open_vulnerabilities_specific_by_type,
    get_reattack_requester,
    get_treatments_count,
    get_updated_manager_mail_content,
    group_vulnerabilities,
    mask_vulnerability,
    send_treatment_change_mail,
)
from vulnerabilities.types import (
    ToolItem,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["finding_id", "expected"],
    [
        [
            "422286126",
            {
                "ports_vulnerabilities": (),
                "lines_vulnerabilities": (
                    Vulnerability(
                        created_by="unittest@fluidattacks.com",
                        created_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        finding_id="422286126",
                        group_name="unittesting",
                        hacker_email="unittest@fluidattacks.com",
                        id="0a848781-b6a4-422e-95fa-692151e6a98z",
                        state=VulnerabilityState(
                            commit="ea871eee64cfd5ce293411efaf4d3b446d04eb4a",
                            modified_by="unittest@fluidattacks.com",
                            modified_date=datetime.fromisoformat(
                                "2020-01-03T17:46:10+00:00"
                            ),
                            source=Source.ASM,
                            specific="12",
                            status=VulnerabilityStateStatus.VULNERABLE,
                            reasons=None,
                            tool=VulnerabilityTool(
                                name="tool-2",
                                impact=VulnerabilityToolImpact.INDIRECT,
                            ),
                            where="test/data/lib_path/f060/csharp.cs",
                        ),
                        type=VulnerabilityType.LINES,
                        bug_tracking_system_url=None,
                        custom_severity=None,
                        hash=None,
                        stream=None,
                        tags=None,
                        treatment=VulnerabilityTreatment(
                            modified_date=datetime.fromisoformat(
                                "2020-01-03T17:46:10+00:00"
                            ),
                            status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                            acceptance_status=None,
                            accepted_until=None,
                            justification="test justification",
                            assigned="integratesuser2@gmail.com",
                            modified_by="integratesuser@gmail.com",
                        ),
                        unreliable_indicators=(
                            VulnerabilityUnreliableIndicators(
                                unreliable_efficacy=Decimal("0"),
                                unreliable_last_reattack_date=None,
                                unreliable_last_reattack_requester=None,
                                unreliable_last_requested_reattack_date=None,
                                unreliable_reattack_cycles=0,
                                unreliable_source=Source.ASM,
                                unreliable_treatment_changes=1,
                            )
                        ),
                        verification=None,
                        zero_risk=None,
                    ),
                ),
                "inputs_vulnerabilities": (),
            },
        ],
        [
            "988493279",
            {
                "ports_vulnerabilities": (
                    Vulnerability(
                        created_by="unittest@fluidattacks.com",
                        created_date=datetime.fromisoformat(
                            "2019-04-08T00:45:15+00:00"
                        ),
                        finding_id="988493279",
                        group_name="unittesting",
                        hacker_email="unittest@fluidattacks.com",
                        id="47ce0fb0-4108-49b0-93cc-160dce8168a6",
                        state=VulnerabilityState(
                            commit=None,
                            modified_by="unittest@fluidattacks.com",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T00:45:15+00:00"
                            ),
                            source=Source.ASM,
                            specific="8888",
                            status=VulnerabilityStateStatus.VULNERABLE,
                            reasons=None,
                            tool=VulnerabilityTool(
                                name="tool-1",
                                impact=VulnerabilityToolImpact.INDIRECT,
                            ),
                            where="192.168.1.19",
                        ),
                        type=VulnerabilityType.PORTS,
                        bug_tracking_system_url=None,
                        custom_severity=None,
                        hash=None,
                        root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                        stream=None,
                        tags=None,
                        treatment=VulnerabilityTreatment(
                            modified_date=datetime.fromisoformat(
                                "2020-10-08T00:59:06+00:00"
                            ),
                            status=(
                                VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
                            ),
                            acceptance_status=(
                                VulnerabilityAcceptanceStatus.APPROVED
                            ),
                            accepted_until=None,
                            justification=(
                                "Observations about permanently accepted"
                            ),
                            assigned="integratesuser@gmail.com",
                            modified_by="integratesuser@gmail.com",
                        ),
                        unreliable_indicators=(
                            VulnerabilityUnreliableIndicators(
                                unreliable_efficacy=Decimal("0"),
                                unreliable_last_reattack_date=None,
                                unreliable_last_reattack_requester=None,
                                unreliable_last_requested_reattack_date=None,
                                unreliable_reattack_cycles=0,
                                unreliable_source=Source.ASM,
                                unreliable_treatment_changes=2,
                            )
                        ),
                        verification=None,
                        zero_risk=None,
                    ),
                ),
                "lines_vulnerabilities": (),
                "inputs_vulnerabilities": (),
            },
        ],
    ],
)
@patch(
    get_mocked_path("loaders.finding_vulnerabilities_released_nzr.load"),
    new_callable=AsyncMock,
)
async def test_get_open_vulnerabilities_specific_by_type(
    mock_loaders_finding_vulnerabilities_released_nzr: AsyncMock,
    finding_id: str,
    expected: dict[str, tuple[Vulnerability, ...]],
) -> None:

    mocked_objects, mocked_paths, mocks_args = [
        [mock_loaders_finding_vulnerabilities_released_nzr],
        ["loaders.finding_vulnerabilities_released_nzr.load"],
        [[finding_id]],
    ]

    assert set_mocks_return_values(
        mocked_objects=mocked_objects,
        paths_list=mocked_paths,
        mocks_args=mocks_args,
    )
    loaders = get_new_context()
    result = await get_open_vulnerabilities_specific_by_type(
        loaders, finding_id
    )
    assert all(mock_object.called is True for mock_object in mocked_objects)
    assert result == expected


async def test_get_reattack_requester() -> None:
    loaders = get_new_context()
    vulnerability = await loaders.vulnerability.load(
        "3bcdb384-5547-4170-a0b6-3b397a245465"
    )
    assert vulnerability
    requester = await get_reattack_requester(
        loaders,
        vuln=vulnerability,
    )
    assert requester == "integratesuser@gmail.com"


@pytest.mark.parametrize(
    ["finding_id", "expected"],
    [
        ["988493279", [0, 1, 0, 0]],
        ["422286126", [0, 0, 1, 0]],
    ],
)
async def test_get_treatments(finding_id: str, expected: list[int]) -> None:
    context = get_new_context()
    finding_vulns_loader = context.finding_vulnerabilities_released_nzr
    vulns = await finding_vulns_loader.load(finding_id)
    treatments = get_treatments_count(vulns)
    assert treatments.accepted == expected[0]
    assert treatments.accepted_undefined == expected[1]
    assert treatments.in_progress == expected[2]
    assert treatments.untreated == expected[3]


@pytest.mark.parametrize(
    ("vulnerabilities"),
    (
        (
            dict(
                ports=[],
                lines=[
                    dict(
                        path="test/data/lib_path/f060/csharp.cs",
                        line="12",
                        state="open",
                        source="analyst",
                        tool=ToolItem(name="tool-2", impact="indirect"),
                        commit_hash="ea871ee",
                    )
                ],
                inputs=[
                    dict(
                        url="https://example.com",
                        field="phone",
                        state="open",
                        source="analyst",
                        tool=ToolItem(name="tool-2", impact="indirect"),
                    )
                ],
            )
        ),
    ),
)
async def test_get_updated_manager_mail_content(
    vulnerabilities: dict[str, list[dict[str, Union[str, ToolItem]]]],
) -> None:
    test_data = get_updated_manager_mail_content(vulnerabilities)
    expected_output = (
        "test/data/lib_path/f060/csharp.cs (12)\nhttps://example.com (phone)\n"
    )
    assert test_data == expected_output


async def test_group_vulnerabilities() -> None:
    loaders = get_new_context()
    vulns = await loaders.finding_vulnerabilities_all.load("422286126")
    test_data = group_vulnerabilities(tuple(vulns))
    expected_output = (
        Vulnerability(
            created_by="unittest@fluidattacks.com",
            created_date=datetime.fromisoformat("2020-01-03T17:46:10+00:00"),
            finding_id="422286126",
            group_name="unittesting",
            hacker_email="unittest@fluidattacks.com",
            id="0a848781-b6a4-422e-95fa-692151e6a98z",
            state=VulnerabilityState(
                modified_by="unittest@fluidattacks.com",
                modified_date=datetime.fromisoformat(
                    "2020-01-03T17:46:10+00:00"
                ),
                source=Source.ASM,
                specific="12",
                status=VulnerabilityStateStatus.VULNERABLE,
                where="test/data/lib_path/f060/csharp.cs",
                commit="ea871ee",
                reasons=None,
                tool=VulnerabilityTool(
                    name="tool-2", impact=VulnerabilityToolImpact.INDIRECT
                ),
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
            treatment=None,
            unreliable_indicators=VulnerabilityUnreliableIndicators(
                unreliable_closing_date=None,
                unreliable_source=Source.ASM,
                unreliable_efficacy=None,
                unreliable_last_reattack_date=None,
                unreliable_last_reattack_requester=None,
                unreliable_last_requested_reattack_date=None,
                unreliable_reattack_cycles=None,
                unreliable_treatment_changes=None,
            ),
            verification=None,
            zero_risk=None,
        ),
        Vulnerability(
            created_by="test@unittesting.com",
            created_date=datetime.fromisoformat("2020-09-09T21:01:26+00:00"),
            finding_id="422286126",
            group_name="unittesting",
            hacker_email="test@unittesting.com",
            id="80d6a69f-a376-46be-98cd-2fdedcffdcc0",
            state=VulnerabilityState(
                modified_by="test@unittesting.com",
                modified_date=datetime.fromisoformat(
                    "2020-09-09T21:01:26+00:00"
                ),
                source=Source.ASM,
                specific="phone",
                status=VulnerabilityStateStatus.VULNERABLE,
                where="https://example.com",
                commit=None,
                reasons=None,
                tool=VulnerabilityTool(
                    name="tool-2", impact=VulnerabilityToolImpact.INDIRECT
                ),
            ),
            type=VulnerabilityType.INPUTS,
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
            treatment=None,
            unreliable_indicators=VulnerabilityUnreliableIndicators(
                unreliable_closing_date=None,
                unreliable_source=Source.ASM,
                unreliable_efficacy=None,
                unreliable_last_reattack_date=None,
                unreliable_last_reattack_requester=None,
                unreliable_last_requested_reattack_date=None,
                unreliable_reattack_cycles=None,
                unreliable_treatment_changes=None,
            ),
            verification=None,
            zero_risk=None,
        ),
    )
    assert test_data == expected_output


@pytest.mark.parametrize(
    ["email", "vulnerability"],
    [
        [
            "integratesuser@gmail.com",
            Vulnerability(
                created_by="test@unittesting.com",
                created_date=datetime.fromisoformat(
                    "2020-09-09T21:01:26+00:00"
                ),
                finding_id="422286126",
                group_name="unittesting",
                hacker_email="test@unittesting.com",
                id="80d6a69f-a376-46be-98cd-2fdedcffdcc0",
                state=VulnerabilityState(
                    modified_by="test@unittesting.com",
                    modified_date=datetime.fromisoformat(
                        "2020-09-09T21:01:26+00:00"
                    ),
                    source=Source.ASM,
                    specific="phone",
                    status=VulnerabilityStateStatus.VULNERABLE,
                    where="https://example.com",
                    commit=None,
                    reasons=None,
                    other_reason=None,
                    tool=VulnerabilityTool(
                        name="tool-2",
                        impact=VulnerabilityToolImpact.INDIRECT,
                    ),
                    snippet=None,
                ),
                type=VulnerabilityType.INPUTS,
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
                        "2020-11-23T17:46:10+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                    acceptance_status=None,
                    accepted_until=None,
                    justification="This is a treatment justification",
                    assigned="integratesuser@gmail.com",
                    modified_by="integratesuser2@gmail.com",
                ),
                unreliable_indicators=VulnerabilityUnreliableIndicators(
                    unreliable_closing_date=None,
                    unreliable_source=Source.ASM,
                    unreliable_efficacy=Decimal("0"),
                    unreliable_last_reattack_date=None,
                    unreliable_last_reattack_requester=None,
                    unreliable_last_requested_reattack_date=None,
                    unreliable_reattack_cycles=0,
                    unreliable_treatment_changes=1,
                ),
                verification=None,
                zero_risk=VulnerabilityZeroRisk(
                    comment_id="123456",
                    modified_by="test@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2020-09-09T21:01:26+00:00"
                    ),
                    status=VulnerabilityZeroRiskStatus.CONFIRMED,
                ),
            ),
        ],
    ],
)
@patch(get_mocked_path("vulns_model.remove"), new_callable=AsyncMock)
@patch(get_mocked_path("loaders.finding.load"), new_callable=AsyncMock)
async def test_mask_vulnerability(
    mock_loaders_finding: AsyncMock,
    mock_vulns_model_remove: AsyncMock,
    email: str,
    vulnerability: Vulnerability,
) -> None:

    mocked_objects, mocked_paths, mocks_args = [
        [
            mock_loaders_finding,
            mock_vulns_model_remove,
        ],
        [
            "loaders.finding.load",
            "vulns_model.remove",
        ],
        [
            [vulnerability.finding_id],
            [vulnerability.id],
        ],
    ]

    assert set_mocks_return_values(
        mocked_objects=mocked_objects,
        paths_list=mocked_paths,
        mocks_args=mocks_args,
    )

    loaders = get_new_context()

    await mask_vulnerability(
        loaders=loaders,
        email=email,
        finding_id=vulnerability.finding_id,
        vulnerability=vulnerability,
    )

    assert all(mock_object.called is True for mock_object in mocked_objects)


@freeze_time("2020-10-08")
@pytest.mark.parametrize(
    ["finding_id", "expected"],
    [
        ["988493279", True],
        ["463461507", False],
    ],
)
async def test_send_treatment_change_mail(
    finding_id: str, expected: bool
) -> None:
    context = get_new_context()
    group_name = "dummy"
    finding_title = "dummy"
    modified_by = "unittest@fluidattacks.com"
    assigned = "vulnmanager@gmail.com"
    justification = "test"
    assert (
        await send_treatment_change_mail(
            loaders=context,
            assigned=assigned,
            finding_id=finding_id,
            finding_title=finding_title,
            group_name=group_name,
            justification=justification,
            min_date=get_now_minus_delta(days=1),
            modified_by=modified_by,
        )
        == expected
    )
