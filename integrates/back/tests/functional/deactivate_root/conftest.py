from back.tests import (
    db,
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
    FindingEvidence,
    FindingEvidences,
    FindingState,
    FindingStatus,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerification,
)
from db_model.roots.types import (
    GitEnvironmentUrl,
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
    IPRootItem,
    IPRootMetadata,
    IPRootState,
    MachineGitRootExecution,
    URLRootItem,
    URLRootMetadata,
    URLRootState,
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
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("deactivate_root")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    test_email = "admin@gmail.com"
    test_date = "2020-11-19T13:37:10+00:00"
    test_status = "ACTIVE"
    data: Dict[str, Any] = {
        "roots": (
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date=test_date,
                    reason="root creation",
                    status=GitCloningStatus("UNKNOWN"),
                ),
                group_name="group1",
                id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                machine_execution=MachineGitRootExecution(
                    queue_date="2021-10-08T16:58:12.499243",
                    finding_code="F122",
                    job_id="78c546bh-dgf5-47e4-a7b3-4a1ebbsd0623",
                ),
                metadata=GitRootMetadata(type="Git"),
                state=GitRootState(
                    branch="master",
                    environment="production",
                    environment_urls=["https://test.com"],
                    git_environment_urls=[
                        GitEnvironmentUrl(url="https://test.com")
                    ],
                    gitignore=["bower_components/*", "node_modules/*"],
                    includes_health_check=True,
                    modified_by=test_email,
                    modified_date=test_date,
                    nickname="nickname",
                    other=None,
                    reason=None,
                    status=test_status,
                    url="https://gitlab.com/fluidattacks/product",
                ),
            ),
            IPRootItem(
                group_name="group2",
                id="83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
                metadata=IPRootMetadata(type="IP"),
                state=IPRootState(
                    address="192.168.1.1",
                    modified_by=test_email,
                    modified_date=test_date,
                    nickname="deactivate_ip_1",
                    other=None,
                    port="8080",
                    reason=None,
                    status=test_status,
                ),
            ),
            URLRootItem(
                group_name="group2",
                id="eee8b331-98b9-4e32-a3c7-ec22bd244ae8",
                metadata=URLRootMetadata(type="URL"),
                state=URLRootState(
                    host="app.fluidattacks.com",
                    modified_by=test_email,
                    modified_date=test_date,
                    nickname="deactivate_url_1",
                    other=None,
                    path="/",
                    port="8080",
                    protocol="HTTPS",
                    reason=None,
                    status=test_status,
                ),
            ),
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date=test_date,
                    reason="root creation",
                    status=GitCloningStatus("UNKNOWN"),
                ),
                group_name="group2",
                id="702b81b3-d741-4699-9173-ecbc30bfb0cb",
                machine_execution=MachineGitRootExecution(
                    queue_date="2021-10-08T16:58:12.499243",
                    finding_code="F122",
                    job_id="78c546bh-dgf5-47e4-a7b3-4a1ebbsd0623",
                ),
                metadata=GitRootMetadata(type="Git"),
                state=GitRootState(
                    branch="master",
                    environment="production",
                    environment_urls=["https://test.com"],
                    git_environment_urls=[
                        GitEnvironmentUrl(url="https://test.com")
                    ],
                    gitignore=["bower_components/*", "node_modules/*"],
                    includes_health_check=True,
                    modified_by=test_email,
                    modified_date=test_date,
                    nickname="nickname",
                    other=None,
                    reason=None,
                    status=test_status,
                    url="https://gitlab.com/fluidattacks/repo",
                ),
            ),
            IPRootItem(
                group_name="group1",
                id="44db9bee-c97d-4161-98c6-f124d7dc9a41",
                metadata=IPRootMetadata(type="IP"),
                state=IPRootState(
                    # FP: local testing
                    address="192.168.1.2",  # NOSONAR
                    modified_by=test_email,
                    modified_date=test_date,
                    nickname="deactivate_ip_2",
                    other=None,
                    port="8080",
                    reason=None,
                    status=test_status,
                ),
            ),
            URLRootItem(
                group_name="group1",
                id="bd4e5e66-da26-4274-87ed-17de7c3bc2f1",
                metadata=URLRootMetadata(type="URL"),
                state=URLRootState(
                    host="test.fluidattacks.com",
                    modified_by=test_email,
                    modified_date=test_date,
                    nickname="deactivate_url_2",
                    other=None,
                    path="/",
                    port="8080",
                    protocol="HTTPS",
                    reason=None,
                    status=test_status,
                ),
            ),
        ),
        "findings": [
            {
                "finding": Finding(
                    id="475041521",
                    group_name="group1",
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="060. Insecure service configuration - Host verification",
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
                    attack_vector_description="This is an updated attack vector",
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
                    unreliable_is_verified=False,
                    unreliable_open_vulnerabilities=5,
                    unreliable_newest_vulnerability_report_date="2020-12-26T05:45:00+00:00",
                    unreliable_oldest_open_vulnerability_report_date="2020-02-24T05:45:00+00:00",
                    unreliable_oldest_vulnerability_report_date="2018-04-01T05:45:00+00:00",
                    unreliable_status=FindingStatus.OPEN,
                    unreliable_where="192.168.1.2",
                ),
            },
            {
                "finding": Finding(
                    id="575041531",
                    group_name="group1",
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="001. SQL injection - C Sharp SQL API",
                    recommendation="Updated recommendation",
                    description="I just have updated the description",
                    hacker_email="test1@gmail.com",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.1"),
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
                    requirements="REQ.0132. Passwords (phrase type) "
                    "must be at least 3 words long.",
                    threat="Updated threat",
                    attack_vector_description="This is an updated attack vector",
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
                "historic_verification": [],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=3,
                    unreliable_is_verified=False,
                    unreliable_open_vulnerabilities=5,
                    unreliable_newest_vulnerability_report_date="2020-12-26T05:45:00+00:00",
                    unreliable_oldest_open_vulnerability_report_date="2020-02-24T05:45:00+00:00",
                    unreliable_oldest_vulnerability_report_date="2018-04-01T05:45:00+00:00",
                    unreliable_status=FindingStatus.OPEN,
                    unreliable_where="192.168.1.2",
                ),
            },
            {
                "finding": Finding(
                    id="475041531",
                    group_name="group1",
                    evidences=FindingEvidences(
                        evidence1=FindingEvidence(
                            description="evidence1",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence1",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                        evidence2=FindingEvidence(
                            description="evidence2",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence2",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                        evidence3=FindingEvidence(
                            description="evidence3",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence3",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                        evidence4=FindingEvidence(
                            description="evidence4",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence4",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                        evidence5=FindingEvidence(
                            description="evidence5",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-evidence5",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                        exploitation=FindingEvidence(
                            description="exploitation",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-exploitation",
                            modified_date="2010-11-19T13:37:10+00:00",
                        ),
                        animation=FindingEvidence(
                            description="animation",
                            url="group1-3c475384-834c-47b0-ac71-a41a022e401c-animation",
                            modified_date="2020-11-19T13:37:10+00:00",
                        ),
                    ),
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date="2017-04-08T00:45:11+00:00",
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="001. SQL injection - C Sharp SQL API",
                    recommendation="Updated recommendation",
                    description="I just have updated the description",
                    hacker_email="test1@gmail.com",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.1"),
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
                    requirements="REQ.0132. Passwords (phrase type) "
                    "must be at least 3 words long.",
                    threat="Updated threat",
                    attack_vector_description="This is an updated attack vector",
                ),
                "historic_state": [],
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
                    unreliable_is_verified=False,
                    unreliable_open_vulnerabilities=5,
                    unreliable_newest_vulnerability_report_date="2020-12-26T05:45:00+00:00",
                    unreliable_oldest_open_vulnerability_report_date="2020-02-24T05:45:00+00:00",
                    unreliable_oldest_vulnerability_report_date="2018-04-01T05:45:00+00:00",
                    unreliable_status=FindingStatus.OPEN,
                    unreliable_where="192.168.1.2",
                ),
            },
        ],
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    finding_id="475041521",
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
                    ),
                    type=VulnerabilityType.PORTS,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_report_date="2018-04-08T00:45:13+00:00",
                        unreliable_source=Source.ASM,
                    ),
                    where="192.168.1.20",
                    root_id="83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="475041521",
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
                    ),
                    where="192.168.1.1",
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="475041521",
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
                    ),
                    where="192.168.1.2",
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    finding_id="475041521",
                    id="6401bc87-8633-4a4a-8d8e-7dae0ca57e6a",
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
                    ),
                    where="192.168.1.3",
                    root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                ),
            },
        ],
    }

    return await db.populate({**generic_data["db_data"], **data})
