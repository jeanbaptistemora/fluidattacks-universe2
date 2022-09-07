# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test import (
    db,
)
from collections import (
    defaultdict,
)
from db_model.enrollment.types import (
    Enrollment,
    Trial,
)
from db_model.enums import (
    GitCloningStatus,
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
    FindingState,
    FindingStatus,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerification,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
    RootEnvironmentUrl,
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
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("me")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "enrollments": (
            Enrollment(
                email="user@gmail.com",
                enrolled=True,
                trial=Trial(
                    completed=True,
                    extension_date="2017-04-06T00:45:11+00:00",
                    extension_days=5,
                    start_date="2017-04-06T00:45:11+00:00",
                ),
            ),
        ),
        "findings": [
            {
                "finding": Finding(
                    id="475041521",
                    group_name="group1",
                    state=FindingState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2017-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title=(
                        "060. Insecure service configuration - "
                        "Host verification"
                    ),
                    recommendation="Updated recommendation",
                    description="I just have updated the description",
                    hacker_email=generic_data["global_vars"]["admin_email"],
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.2"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1.5"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("0.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_integrity_impact=Decimal("0"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_severity_scope=Decimal("0"),
                        modified_privileges_required=Decimal("0.27"),
                        modified_attack_vector=Decimal("0.85"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        privileges_required=Decimal("0.62"),
                        severity_scope=Decimal("1.2"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("1"),
                        user_interaction=Decimal("0.85"),
                    ),
                    requirements="R359. Avoid using generic exceptions.",
                    threat="Autenticated attacker from the Internet.",
                    attack_vector_description=(
                        "This is an updated attack vector"
                    ),
                ),
                "historic_state": [
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:12+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:13+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.REJECTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:14+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2018-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                    ),
                ],
                "historic_verification": [
                    FindingVerification(
                        comment_id="42343434",
                        modified_by="test1@gmail.com",
                        modified_date="2020-01-01T00:45:12+00:00",
                        status=FindingVerificationStatus.REQUESTED,
                        vulnerability_ids={
                            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
                            "uuid2",
                        },
                    )
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=3,
                    unreliable_open_vulnerabilities=5,
                    unreliable_newest_vulnerability_report_date=(
                        "2020-12-26T05:45:00+00:00"
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        "2020-02-24T05:45:00+00:00"
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        "2018-04-01T05:45:00+00:00"
                    ),
                    unreliable_status=FindingStatus.OPEN,
                    unreliable_where="192.168.1.2",
                ),
            },
            {
                "finding": Finding(
                    id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    state=FindingState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2017-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="001. SQL injection - C Sharp SQL API",
                    recommendation="Updated recommendation",
                    description="I just have updated the description",
                    hacker_email=generic_data["global_vars"]["admin_email"],
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.2"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1.5"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("0.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_integrity_impact=Decimal("0"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_severity_scope=Decimal("0"),
                        modified_privileges_required=Decimal("0.27"),
                        modified_attack_vector=Decimal("0.85"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        privileges_required=Decimal("0.62"),
                        severity_scope=Decimal("1.2"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("1"),
                        user_interaction=Decimal("0.85"),
                    ),
                    requirements=(
                        "REQ.0132. Passwords (phrase type) "
                        "must be at least 3 words long."
                    ),
                    threat="Updated threat",
                    attack_vector_description="This is an updated attack vect",
                ),
                "historic_state": [
                    FindingState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2017-04-08T00:45:12+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                ],
                "historic_verification": [
                    FindingVerification(
                        comment_id="42343434",
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2020-01-01T00:45:12+00:00",
                        status=FindingVerificationStatus.REQUESTED,
                        vulnerability_ids={
                            "48780201-b087-43c5-9882-a5c65dec6efb",
                        },
                    )
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=3,
                    unreliable_open_vulnerabilities=5,
                    unreliable_newest_vulnerability_report_date=(
                        "2020-12-26T05:45:00+00:00"
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        "2020-02-24T05:45:00+00:00"
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        "2018-04-01T05:45:00+00:00"
                    ),
                    unreliable_status=FindingStatus.OPEN,
                    unreliable_where="192.168.1.2",
                ),
            },
        ],
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    finding_id="475041521",
                    group_name="group1",
                    hacker_email=generic_data["global_vars"]["admin_email"],
                    id="be09edb7-cd5c-47ed-bee4-97c645acdce8",
                    specific="9999",
                    state=VulnerabilityState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2018-04-08T00:45:13+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:45:14+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                        assigned=generic_data["global_vars"][
                            "vulnerability_manager_email"
                        ],
                        modified_by=generic_data["global_vars"][
                            "user_manager_email"
                        ],
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_report_date="2018-04-08T00:45:13+00:00",
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                    where="192.168.1.20",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="475041521",
                    group_name="group1",
                    hacker_email=generic_data["global_vars"]["admin_email"],
                    id="6401bc87-8633-4a4a-8d8e-7dae0ca57e6a",
                    specific="2320",
                    state=VulnerabilityState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2018-04-08T00:45:15+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.CLOSED,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-09T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        accepted_until="2018-04-09T00:45:11+00:00",
                        justification="justification",
                        assigned=generic_data["global_vars"]["user_email"],
                        modified_by=generic_data["global_vars"][
                            "user_manager_email"
                        ],
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_report_date="2018-04-08T00:45:15+00:00",
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                    where="192.168.1.1",
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="475041521",
                    group_name="group1",
                    hacker_email=generic_data["global_vars"]["admin_email"],
                    id="6401bc87-8633-4a4a-8d8e-7dae0ca57e6b",
                    specific="2321",
                    state=VulnerabilityState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2018-04-08T00:45:15+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-09T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        accepted_until="2018-04-09T00:45:11+00:00",
                        justification="justification",
                        assigned=generic_data["global_vars"]["user_email"],
                        modified_by=generic_data["global_vars"][
                            "user_manager_email"
                        ],
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_report_date="2018-04-08T00:45:15+00:00",
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                    where="192.168.1.2",
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="475041521",
                    group_name="group1",
                    hacker_email=generic_data["global_vars"]["admin_email"],
                    id="de70c2f7-7ec7-49aa-9a84-aff4fbe5d1ad",
                    specific="2322",
                    state=VulnerabilityState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2018-04-08T00:45:16+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.OPEN,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-09T00:45:11+00:00",
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        accepted_until="2018-04-09T00:45:11+00:00",
                        justification="justification",
                        assigned=generic_data["global_vars"][
                            "user_manager_email"
                        ],
                        modified_by=generic_data["global_vars"][
                            "user_manager_email"
                        ],
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_report_date="2018-04-08T00:45:16+00:00",
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=1,
                    ),
                    where="192.168.1.3",
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email=generic_data["global_vars"]["admin_email"],
                    id="48780201-b087-43c5-9882-a5c65dec6efb",
                    specific="9999",
                    state=VulnerabilityState(
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date="2018-04-08T00:45:14+00:00",
                        source=Source.ASM,
                        status=VulnerabilityStateStatus.CLOSED,
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date="2018-04-08T00:45:14+00:00",
                        status=VulnerabilityTreatmentStatus.NEW,
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_report_date="2018-04-08T00:45:14+00:00",
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                    where="192.168.1.20",
                ),
            },
        ],
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date="2020-11-19T13:37:10+00:00",
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    group_name="group1",
                    id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        environment_urls=["https://.com"],
                        git_environment_urls=[
                            RootEnvironmentUrl(
                                url="https://test.com",
                                id="78dd64d3198473115a7f5263d27bed15f9f2fc07",
                            )
                        ],
                        gitignore=["bower_components/*", "node_modules/*"],
                        includes_health_check=True,
                        modified_by="admin@gmail.com",
                        modified_date="2020-11-19T13:37:10+00:00",
                        nickname="",
                        other=None,
                        reason=None,
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/universe",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
        ],
        "policies": [
            {
                "level": "group",
                "subject": generic_data["global_vars"]["admin_email"],
                "object": "group2",
                "role": "admin",
            },
            {
                "level": "group",
                "subject": generic_data["global_vars"]["admin_email"],
                "object": "group3",
                "role": "admin",
            },
        ],
    }

    merge_dict = defaultdict(list)
    for dict_data in (generic_data["db_data"], data):
        for key, value in dict_data.items():
            merge_dict[key].extend(value)

    return await db.populate(merge_dict)
