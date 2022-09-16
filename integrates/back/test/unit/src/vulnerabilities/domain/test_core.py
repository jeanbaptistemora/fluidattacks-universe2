# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityToolImpact,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTool,
    VulnerabilityTreatment,
    VulnerabilityTreatmentStatus,
    VulnerabilityUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from freezegun import (  # type: ignore
    freeze_time,
)
from newutils.datetime import (
    get_now_minus_delta,
)
from newutils.vulnerabilities import (
    format_vulnerabilities,
)
import pytest
from typing import (
    Dict,
    List,
    Tuple,
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

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["finding_id", "expected"],
    [
        [
            "988493279",
            {
                "ports_vulnerabilities": (
                    Vulnerability(
                        created_by="unittest@fluidattacks.com",
                        created_date="2019-04-08T00:45:15+00:00",
                        finding_id="988493279",
                        group_name="unittesting",
                        hacker_email="unittest@fluidattacks.com",
                        id="47ce0fb0-4108-49b0-93cc-160dce8168a6",
                        specific="8888",
                        state=VulnerabilityState(
                            modified_by="unittest@fluidattacks.com",
                            modified_date="2019-04-08T00:45:15+00:00",
                            source=Source.ASM,
                            status=VulnerabilityStateStatus.OPEN,
                            justification=None,
                            tool=VulnerabilityTool(
                                name="tool-1",
                                impact=VulnerabilityToolImpact.INDIRECT,
                            ),
                        ),
                        type=VulnerabilityType.PORTS,
                        where="192.168.1.19",
                        bug_tracking_system_url=None,
                        commit=None,
                        custom_severity=None,
                        hash=None,
                        stream=None,
                        tags=None,
                        treatment=VulnerabilityTreatment(
                            modified_date="2020-10-08T00:59:06+00:00",
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
        [
            "422286126",
            {
                "ports_vulnerabilities": (),
                "lines_vulnerabilities": (
                    Vulnerability(
                        created_by="unittest@fluidattacks.com",
                        created_date="2020-01-03T17:46:10+00:00",
                        finding_id="422286126",
                        group_name="unittesting",
                        hacker_email="unittest@fluidattacks.com",
                        id="0a848781-b6a4-422e-95fa-692151e6a98z",
                        specific="12",
                        state=VulnerabilityState(
                            modified_by="unittest@fluidattacks.com",
                            modified_date="2020-01-03T17:46:10+00:00",
                            source=Source.ASM,
                            status=VulnerabilityStateStatus.OPEN,
                            justification=None,
                            tool=VulnerabilityTool(
                                name="tool-2",
                                impact=VulnerabilityToolImpact.INDIRECT,
                            ),
                        ),
                        type=VulnerabilityType.LINES,
                        where="test/data/lib_path/f060/csharp.cs",
                        bug_tracking_system_url=None,
                        commit="ea871eee64cfd5ce293411efaf4d3b446d04eb4a",
                        custom_severity=None,
                        hash=None,
                        stream=None,
                        tags=None,
                        treatment=VulnerabilityTreatment(
                            modified_date="2020-01-03T17:46:10+00:00",
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
    ],
)
async def test_get_open_vulnerabilities_specific_by_type(
    finding_id: str, expected: Dict[str, Tuple[Dict[str, str], ...]]
) -> None:
    loaders: Dataloaders = get_new_context()
    results = await get_open_vulnerabilities_specific_by_type(
        loaders, finding_id
    )
    assert results == expected


async def test_get_reattack_requester() -> None:
    loaders = get_new_context()
    vulnerability: Vulnerability = await loaders.vulnerability.load(
        "3bcdb384-5547-4170-a0b6-3b397a245465"
    )
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
async def test_get_treatments(finding_id: str, expected: List[int]) -> None:
    context = get_new_context()
    finding_vulns_loader = context.finding_vulnerabilities_nzr
    vulns = await finding_vulns_loader.load(finding_id)
    treatments = get_treatments_count(vulns)
    assert treatments.accepted == expected[0]
    assert treatments.accepted_undefined == expected[1]
    assert treatments.in_progress == expected[2]
    assert treatments.new == expected[3]


@pytest.mark.changes_db
async def test_get_updated_manager_mail_content() -> None:
    finding_id = "422286126"
    loaders = get_new_context()
    finding_vulns = await loaders.finding_vulnerabilities_all.load(finding_id)
    grouped_vulns = group_vulnerabilities(finding_vulns)
    vulns_data = await format_vulnerabilities(
        "unittesting", loaders, grouped_vulns
    )
    test_data = get_updated_manager_mail_content(vulns_data)
    expected_output = "- test/data/lib_path/f060/csharp.cs (12)\n- https://example.com (phone)\n"  # noqa
    assert test_data == expected_output


async def test_group_vulnerabilities() -> None:
    loaders = get_new_context()
    vulns = await loaders.finding_vulnerabilities_all.load("422286126")
    test_data = group_vulnerabilities(vulns)
    expected_output = (
        Vulnerability(
            created_by="unittest@fluidattacks.com",
            created_date="2020-01-03T17:46:10+00:00",
            finding_id="422286126",
            group_name="unittesting",
            hacker_email="unittest@fluidattacks.com",
            id="0a848781-b6a4-422e-95fa-692151e6a98z",
            specific="12",
            state=VulnerabilityState(
                modified_by="unittest@fluidattacks.com",
                modified_date="2020-01-03T17:46:10+00:00",
                source=Source.ASM,
                status=VulnerabilityStateStatus.OPEN,
                tool=VulnerabilityTool(
                    name="tool-2",
                    impact=VulnerabilityToolImpact.INDIRECT,
                ),
            ),
            type=VulnerabilityType.LINES,
            where="test/data/lib_path/f060/csharp.cs",
            commit="ea871ee",
        ),
        Vulnerability(
            created_by="test@unittesting.com",
            created_date="2020-09-09T21:01:26+00:00",
            finding_id="422286126",
            group_name="unittesting",
            hacker_email="test@unittesting.com",
            id="80d6a69f-a376-46be-98cd-2fdedcffdcc0",
            specific="phone",
            state=VulnerabilityState(
                modified_by="test@unittesting.com",
                modified_date="2020-09-09T21:01:26+00:00",
                source=Source.ASM,
                status=VulnerabilityStateStatus.OPEN,
                tool=VulnerabilityTool(
                    name="tool-2",
                    impact=VulnerabilityToolImpact.INDIRECT,
                ),
            ),
            type=VulnerabilityType.INPUTS,
            where="https://example.com",
            commit=None,
        ),
    )
    assert test_data == expected_output


@pytest.mark.changes_db
async def test_mask_vulnerability() -> None:
    vuln_id = "80d6a69f-a376-46be-98cd-2fdedcffdcc0"
    loaders: Dataloaders = get_new_context()
    vuln: Vulnerability = await loaders.vulnerability.load(vuln_id)
    assert vuln.specific == "phone"
    assert vuln.where == "https://example.com"
    assert vuln.treatment == VulnerabilityTreatment(
        justification="This is a treatment justification",
        assigned="integratesuser@gmail.com",
        modified_by="integratesuser2@gmail.com",
        modified_date="2020-11-23T17:46:10+00:00",
        status=VulnerabilityTreatmentStatus.IN_PROGRESS,
    )
    await mask_vulnerability(
        loaders=loaders,
        finding_id=vuln.finding_id,
        vulnerability=vuln,
    )


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
