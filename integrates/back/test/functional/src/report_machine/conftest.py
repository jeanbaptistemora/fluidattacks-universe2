# pylint: disable=import-error,too-many-lines
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
    Source,
)
from db_model.findings.enums import (
    FindingStateStatus,
    FindingStatus,
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    FindingEvidence,
    FindingEvidences,
    FindingState,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerification,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupState,
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
from db_model.toe_lines.types import (
    ToeLines,
    ToeLinesState,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
    VulnerabilityVerification,
)
from newutils import (
    machine as machine_utils,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)

CRITERIA_VULNERABILITIES: dict[str, dict[str, Any]] = {
    "001": {
        "en": {
            "title": "SQL injection - C Sharp SQL API",
            "description": "Description sql",
            "impact": "Impact sql",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "es": {
            "title": "SQL injection - C Sharp SQL API",
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "category": "Unexpected Injection",
        "examples": {
            "non_compliant": "non_compliant",
            "compliant": "compliant",
        },
        "remediation_time": "15",
        "score": {
            "base": {
                "attack_vector": "N",
                "attack_complexity": "L",
                "privileges_required": "L",
                "user_interaction": "N",
                "scope": "U",
                "confidentiality": "N",
                "integrity": "L",
                "availability": "N",
            },
            "temporal": {
                "exploit_code_maturity": "U",
                "remediation_level": "O",
                "report_confidence": "R",
            },
        },
        "requirements": ["169", "173"],
        "metadata": {"en": {"details": "details test"}},
    },
    "002": {
        "en": {
            "title": "Asymmetric denial of service",
            "description": "Description sql",
            "impact": "Impact sql",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "es": {
            "title": "Asymmetric denial of service",
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "category": "Unexpected Injection",
        "examples": {
            "non_compliant": "non_compliant",
            "compliant": "compliant",
        },
        "remediation_time": "15",
        "score": {
            "base": {
                "attack_vector": "N",
                "attack_complexity": "L",
                "privileges_required": "L",
                "user_interaction": "N",
                "scope": "U",
                "confidentiality": "N",
                "integrity": "L",
                "availability": "N",
            },
            "temporal": {
                "exploit_code_maturity": "U",
                "remediation_level": "O",
                "report_confidence": "R",
            },
        },
        "requirements": ["169", "173"],
        "metadata": {"en": {"details": "details test"}},
    },
    "011": {
        "en": {
            "title": "Use of software with known vulnerabilities",
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "es": {
            "title": "Use of software with known vulnerabilities",
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "category": "Information Collection",
        "examples": {
            "non_compliant": "non_compliant",
            "compliant": "compliant",
        },
        "remediation_time": "60",
        "score": {
            "base": {
                "attack_vector": "N",
                "attack_complexity": "H",
                "privileges_required": "L",
                "user_interaction": "N",
                "scope": "U",
                "confidentiality": "L",
                "integrity": "L",
                "availability": "L",
            },
            "temporal": {
                "exploit_code_maturity": "P",
                "remediation_level": "O",
                "report_confidence": "C",
            },
        },
        "requirements": ["262"],
        "metadata": {"en": {"details": "__empty__"}},
    },
    "043": {
        "en": {
            "title": (
                "Insecure or unset HTTP headers - Content-Security-Policy"
            ),
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "es": {
            "title": (
                "Insecure or unset HTTP headers - Content-Security-Policy"
            ),
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "category": "Protocol Manipulation",
        "examples": {
            "non_compliant": "non_compliant",
            "compliant": "compliant",
        },
        "remediation_time": "15",
        "score": {
            "base": {
                "attack_vector": "N",
                "attack_complexity": "H",
                "privileges_required": "N",
                "user_interaction": "R",
                "scope": "U",
                "confidentiality": "L",
                "integrity": "L",
                "availability": "N",
            },
            "temporal": {
                "exploit_code_maturity": "P",
                "remediation_level": "O",
                "report_confidence": "C",
            },
        },
        "requirements": ["062", "117", "175", "349"],
        "metadata": {"en": {"details": "__empty__"}},
    },
    "117": {
        "en": {
            "title": "Unverifiable files",
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "es": {
            "title": "Unverifiable files",
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "category": "Functionality Abuse",
        "examples": {
            "non_compliant": "non_compliant",
            "compliant": "compliant",
        },
        "remediation_time": "15",
        "score": {
            "base": {
                "attack_vector": "N",
                "attack_complexity": "H",
                "privileges_required": "L",
                "user_interaction": "N",
                "scope": "U",
                "confidentiality": "N",
                "integrity": "L",
                "availability": "N",
            },
            "temporal": {
                "exploit_code_maturity": "U",
                "remediation_level": "X",
                "report_confidence": "X",
            },
        },
        "requirements": ["323"],
        "metadata": {"en": {"details": "__empty__"}},
    },
    "120": {
        "en": {
            "title": "Improper dependency pinning",
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "es": {
            "title": "Improper dependency pinning",
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "category": "Functionality Abuse",
        "examples": {
            "non_compliant": "non_compliant",
            "compliant": "compliant",
        },
        "remediation_time": "30",
        "score": {
            "base": {
                "attack_vector": "N",
                "attack_complexity": "H",
                "privileges_required": "N",
                "user_interaction": "N",
                "scope": "U",
                "confidentiality": "N",
                "integrity": "L",
                "availability": "N",
            },
            "temporal": {
                "exploit_code_maturity": "U",
                "remediation_level": "X",
                "report_confidence": "X",
            },
        },
        "requirements": ["302"],
        "metadata": {"en": {"details": "__empty__"}},
    },
    "237": {
        "en": {
            "title": "Technical information leak - Print Functions",
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "es": {
            "title": "Technical information leak - Print Functions",
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "category": "Information Collection",
        "examples": {
            "non_compliant": "non_compliant",
            "compliant": "compliant",
        },
        "remediation_time": "15",
        "score": {
            "base": {
                "attack_vector": "L",
                "attack_complexity": "L",
                "privileges_required": "H",
                "user_interaction": "N",
                "scope": "U",
                "confidentiality": "L",
                "integrity": "N",
                "availability": "N",
            },
            "temporal": {
                "exploit_code_maturity": "P",
                "remediation_level": "U",
                "report_confidence": "C",
            },
        },
        "requirements": ["077", "176"],
        "metadata": {"en": {"details": "__empty__"}},
    },
    "128": {
        "en": {
            "title": "Insecurely generated cookies - HttpOnly",
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "es": {
            "title": "Insecurely generated cookies - HttpOnly",
            "description": "Description",
            "impact": "Impact",
            "recommendation": "Recommendation",
            "threat": "Threat",
        },
        "category": "Access Subversion",
        "examples": {
            "non_compliant": "non_compliant",
            "compliant": "compliant",
        },
        "remediation_time": "30",
        "score": {
            "base": {
                "attack_vector": "N",
                "attack_complexity": "H",
                "privileges_required": "N",
                "user_interaction": "R",
                "scope": "U",
                "confidentiality": "L",
                "integrity": "N",
                "availability": "N",
            },
            "temporal": {
                "exploit_code_maturity": "P",
                "remediation_level": "O",
                "report_confidence": "X",
            },
        },
        "requirements": ["029"],
        "metadata": {"en": {"details": "__empty__"}},
    },
}


@pytest.mark.resolver_test_group("report_machine")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "groups": [
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="This is a dummy description",
                    language=GroupLanguage.EN,
                    name="group1",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    business_id="123",
                    business_name="acme",
                    sprint_duration=3,
                ),
            }
        ],
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.OK,
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="group1",
                    id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="nickname",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/nickname",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
                "git_environment_urls": [
                    RootEnvironmentUrl(
                        url="http://localhost:48000/",
                        id="3aca06ef047ca0195f8ffc7ea5b64605b3f779cb",
                        secrets=[],
                    )
                ],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.OK,
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="group1",
                    id="9059f0cb-3b55-404b-8fc5-627171f424ad",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="nickname2",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/nickname2",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
        ],
        "findings": [
            {
                "finding": Finding(
                    id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="001. SQL injection - C Sharp SQL API",
                    recommendation="Updated recommendation",
                    description=CRITERIA_VULNERABILITIES["001"]["en"][
                        "description"
                    ],
                    hacker_email="test1@gmail.com",
                    severity=machine_utils.get_finding_machine_severity(
                        CRITERIA_VULNERABILITIES["001"]
                    ),
                    requirements=(
                        "REQ.0132. Passwords (phrase type) "
                        "must be at least 3 words long."
                    ),
                    threat=CRITERIA_VULNERABILITIES["001"]["en"]["threat"],
                    attack_vector_description=(
                        "This is an updated attack vector"
                    ),
                    evidences=FindingEvidences(
                        evidence5=FindingEvidence(
                            description="evidence5",
                            url=(
                                "group1-3c475384-834c-47b0-ac71-a41a022e401c-"
                                "evidence5"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                        records=FindingEvidence(
                            description="records",
                            url=(
                                "group1-3c475384-834c-47b0-ac71-a41a022e401c-"
                                "records"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2111-11-19T13:37:10+00:00"
                            ),
                        ),
                    ),
                ),
                "historic_state": [
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:12+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:13+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.REJECTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:14+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                    ),
                ],
                "historic_verification": [
                    FindingVerification(
                        comment_id="42343434",
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-01T00:45:12+00:00"
                        ),
                        status=FindingVerificationStatus.REQUESTED,
                        vulnerability_ids={
                            "6dbc13e1-5cfc-3b44-9b70-bb7566c641sz",
                        },
                    )
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=3,
                    unreliable_open_vulnerabilities=5,
                    unreliable_newest_vulnerability_report_date=(
                        datetime.fromisoformat("2020-12-26T05:45:00+00:00")
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        datetime.fromisoformat("2020-02-24T05:45:00+00:00")
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        datetime.fromisoformat("2018-04-01T05:45:00+00:00")
                    ),
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_where="192.168.1.2",
                ),
            },
            {
                "finding": Finding(
                    id="5b274854-f2b3-4832-bd62-9d14caebdcc3",
                    group_name="group1",
                    state=FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="002. Asymmetric denial of service",
                    recommendation="Updated recommendation",
                    description="Another description",
                    hacker_email="test1@gmail.com",
                    severity=machine_utils.get_finding_machine_severity(
                        CRITERIA_VULNERABILITIES["002"]
                    ),
                    requirements="",
                    threat=CRITERIA_VULNERABILITIES["002"]["en"]["threat"],
                    attack_vector_description=(
                        "This is an updated attack vector"
                    ),
                    evidences=FindingEvidences(
                        evidence5=FindingEvidence(
                            description="evidence5",
                            url=(
                                "group1-5b274854-f2b3-4832-bd62-9d14caebdcc3-"
                                "evidence5"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2020-11-19T13:37:10+00:00"
                            ),
                        ),
                        records=FindingEvidence(
                            description="records",
                            url=(
                                "group1-5b274854-f2b3-4832-bd62-9d14caebdcc3-"
                                "records"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2111-11-19T13:37:10+00:00"
                            ),
                        ),
                    ),
                ),
                "historic_state": [
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:12+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:13+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.REJECTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2017-04-08T00:45:14+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                    ),
                ],
                "historic_verification": [
                    FindingVerification(
                        comment_id="42343434",
                        modified_by="test1@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-01T00:45:12+00:00"
                        ),
                        status=FindingVerificationStatus.REQUESTED,
                        vulnerability_ids={
                            "010e196c-b6ce-4231-97b6-12b8ef41870e",
                        },
                    )
                ],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=3,
                    unreliable_open_vulnerabilities=5,
                    unreliable_newest_vulnerability_report_date=(
                        datetime.fromisoformat("2020-12-26T05:45:00+00:00")
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        datetime.fromisoformat("2020-02-24T05:45:00+00:00")
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        datetime.fromisoformat("2018-04-01T05:45:00+00:00")
                    ),
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_where="192.168.1.2",
                ),
            },
            {
                "finding": Finding(
                    id="4629a805-7ce5-4cd1-a39a-4579ec6fd985",
                    group_name="group1",
                    state=FindingState(
                        modified_by="hacker@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-19T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                    title="117. Unverifiable files",
                    recommendation="Recommendation",
                    description=CRITERIA_VULNERABILITIES["117"]["en"][
                        "description"
                    ],
                    hacker_email="hacker@fluidattacks.com",
                    severity=machine_utils.get_finding_machine_severity(
                        CRITERIA_VULNERABILITIES["117"]
                    ),
                    requirements="Requirement",
                    threat=CRITERIA_VULNERABILITIES["117"]["en"]["threat"],
                    attack_vector_description="Attack vector",
                    evidences=FindingEvidences(
                        evidence5=FindingEvidence(
                            description="evidence5",
                            url=(
                                "group1-4629a805-7ce5-4cd1-a39a-4579ec6fd985-"
                                "evidence5"
                            ),
                            modified_date=datetime.fromisoformat(
                                "2022-10-19T05:00:05+00:00"
                            ),
                        ),
                    ),
                ),
                "historic_state": [
                    FindingState(
                        modified_by="hacker@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-19T05:00:15+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    FindingState(
                        modified_by="hacker@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-19T05:00:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                    ),
                ],
                "historic_verification": [],
                "unreliable_indicator": FindingUnreliableIndicatorsToUpdate(
                    unreliable_closed_vulnerabilities=0,
                    unreliable_open_vulnerabilities=1,
                    unreliable_newest_vulnerability_report_date=(
                        datetime.fromisoformat("2022-10-19T05:00:15+00:00")
                    ),
                    unreliable_oldest_open_vulnerability_report_date=(
                        datetime.fromisoformat("2022-10-19T05:00:15+00:00")
                    ),
                    unreliable_oldest_vulnerability_report_date=(
                        datetime.fromisoformat("2022-10-19T05:00:15+00:00")
                    ),
                    unreliable_status=FindingStatus.VULNERABLE,
                    unreliable_where=".project",
                ),
            },
        ],
        "vulnerabilities": [
            {
                "vulnerability": Vulnerability(
                    created_by="machine@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="4dbc03e0-4cfc-4b33-9b70-bb7566c460bd",
                    hash=15417318278186201633,
                    state=VulnerabilityState(
                        modified_by="machine@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.MACHINE,
                        specific="52",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="back/src/model/user/index.js",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="machine@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="4dbc01e0-4cfc-4b77-9b71-bb7566c60bg",
                    hash=8061522565195734354,
                    state=VulnerabilityState(
                        modified_by="machine@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.MACHINE,
                        specific="12",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="back/src/controller/user/index.js",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="machine@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="5dbc02e0-4cfc-4b33-9b70-bb7566c230cv",
                    hash=11980225504472206636,
                    state=VulnerabilityState(
                        modified_by="machine@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.MACHINE,
                        specific="64",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="front/index.html",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="machine@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    finding_id="3c475384-834c-47b0-ac71-a41a022e401c",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="6dbc13e1-5cfc-3b44-9b70-bb7566c641sz",
                    state=VulnerabilityState(
                        modified_by="machine@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.MACHINE,
                        specific="35",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="back/src/index.js",
                    ),
                    hash=3112310311844910506,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="hacker@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-19T05:00:20+00:00"
                    ),
                    finding_id="4629a805-7ce5-4cd1-a39a-4579ec6fd985",
                    group_name="group1",
                    hacker_email="hacker@fluidattacks.com",
                    id="dadb5c43-90ab-47ea-a80f-db89a940cd54",
                    state=VulnerabilityState(
                        modified_by="hacker@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-19T05:00:20+00:00"
                        ),
                        source=Source.ASM,
                        specific="0",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where=".project",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2022-10-19T05:00:20+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.ASM,
                        unreliable_treatment_changes=0,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="machine@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    finding_id="5b274854-f2b3-4832-bd62-9d14caebdcc3",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="59fe52fb-d065-4d23-b42b-5988b960dc59",
                    hash=15417318278186201633,
                    state=VulnerabilityState(
                        modified_by="machine@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.MACHINE,
                        specific="52",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="back/src/model/new_finding/index.js",
                    ),
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
            },
            {
                "vulnerability": Vulnerability(
                    created_by="machine@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-04-08T00:45:15+00:00"
                    ),
                    finding_id="5b274854-f2b3-4832-bd62-9d14caebdcc3",
                    group_name="group1",
                    hacker_email="test1@gmail.com",
                    id="010e196c-b6ce-4231-97b6-12b8ef41870e",
                    state=VulnerabilityState(
                        modified_by="machine@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:15+00:00"
                        ),
                        source=Source.MACHINE,
                        specific="35",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="back/src/new_finding.js",
                    ),
                    hash=3112310311844910506,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                    ),
                    type=VulnerabilityType.LINES,
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_source=Source.MACHINE,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2018-04-09T00:45:11+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                    ),
                    root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                ),
            },
        ],
        "toe_lines": (
            ToeLines(
                filename="nickname/back/src/model/user/index.js",
                group_name="group1",
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                state=ToeLinesState(
                    attacked_at=None,
                    attacked_by="machine@fluidattacks.com",
                    attacked_lines=23,
                    be_present=True,
                    be_present_until=None,
                    comments="",
                    first_attack_at=None,
                    has_vulnerabilities=False,
                    last_author="customer1@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-16T15:41:04+00:00"
                    ),
                    loc=4324,
                    modified_by="machine@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-16T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-01-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=0,
                ),
            ),
            ToeLines(
                filename="back/src/index.js",
                group_name="group1",
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                state=ToeLinesState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-20T05:00:00+00:00"
                    ),
                    attacked_by="machine@fluidattacks.com",
                    attacked_lines=4,
                    be_present=True,
                    be_present_until=None,
                    comments="comment 2",
                    first_attack_at=datetime.fromisoformat(
                        "2020-02-19T15:41:04+00:00"
                    ),
                    has_vulnerabilities=False,
                    last_author="customer2@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    loc=180,
                    modified_by="machine@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-02-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=-1,
                ),
            ),
            ToeLines(
                filename="skims/test/data/lib_path/f011/requirements.txt",
                group_name="group1",
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                state=ToeLinesState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-20T05:00:00+00:00"
                    ),
                    attacked_by="machine@fluidattacks.com",
                    attacked_lines=4,
                    be_present=True,
                    be_present_until=None,
                    comments="comment 2",
                    has_vulnerabilities=False,
                    last_author="customer2@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    loc=180,
                    first_attack_at=datetime.fromisoformat(
                        "2020-02-19T15:41:04+00:00"
                    ),
                    modified_by="machine@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-02-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=-1,
                ),
            ),
            ToeLines(
                filename="front/index.html",
                group_name="group1",
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                state=ToeLinesState(
                    attacked_at=datetime.fromisoformat(
                        "2020-01-14T15:41:04+00:00"
                    ),
                    attacked_by="machine@fluidattacks.com",
                    attacked_lines=120,
                    be_present=True,
                    be_present_until=None,
                    comments="",
                    first_attack_at=datetime.fromisoformat(
                        "2020-01-14T15:41:04+00:00"
                    ),
                    has_vulnerabilities=False,
                    last_author="customer3@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c3",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-16T15:41:04+00:00"
                    ),
                    loc=243,
                    modified_by="machine@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-16T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2019-01-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=80,
                ),
            ),
            ToeLines(
                filename="skims/test/data/lib_path/f011/build.gradle",
                group_name="group1",
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                state=ToeLinesState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-20T05:00:00+00:00"
                    ),
                    attacked_by="machine@fluidattacks.com",
                    attacked_lines=1,
                    be_present=True,
                    be_present_until=None,
                    comments="",
                    first_attack_at=datetime.fromisoformat(
                        "2020-02-19T15:41:04+00:00"
                    ),
                    has_vulnerabilities=False,
                    last_author="customer2@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c5",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    loc=180,
                    modified_by="machine@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-02-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=-1,
                ),
            ),
            ToeLines(
                filename="MyJar.jar",
                group_name="group1",
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                state=ToeLinesState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-20T05:00:00+00:00"
                    ),
                    attacked_by="machine@fluidattacks.com",
                    attacked_lines=1,
                    be_present=True,
                    be_present_until=None,
                    comments="",
                    first_attack_at=datetime.fromisoformat(
                        "2020-02-19T15:41:04+00:00"
                    ),
                    has_vulnerabilities=False,
                    last_author="customer2@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c5",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    loc=180,
                    modified_by="machine@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-02-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=-1,
                ),
            ),
            ToeLines(
                filename="MyJar.class",
                group_name="group1",
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                state=ToeLinesState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-20T05:00:00+00:00"
                    ),
                    attacked_by="machine@fluidattacks.com",
                    attacked_lines=1,
                    be_present=True,
                    be_present_until=None,
                    comments="",
                    first_attack_at=datetime.fromisoformat(
                        "2020-02-19T15:41:04+00:00"
                    ),
                    has_vulnerabilities=False,
                    last_author="customer2@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c5",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    loc=180,
                    modified_by="machine@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-02-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=-1,
                ),
            ),
            ToeLines(
                filename="java_has_print_statements.java",
                group_name="group1",
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                state=ToeLinesState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-20T05:00:00+00:00"
                    ),
                    attacked_by="machine@fluidattacks.com",
                    attacked_lines=30,
                    be_present=True,
                    be_present_until=None,
                    comments="",
                    first_attack_at=datetime.fromisoformat(
                        "2020-02-19T15:41:04+00:00"
                    ),
                    has_vulnerabilities=False,
                    last_author="customer2@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c5",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    loc=180,
                    modified_by="machine@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-02-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=-1,
                ),
            ),
            ToeLines(
                filename="package.json",
                group_name="group1",
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                state=ToeLinesState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-20T05:00:00+00:00"
                    ),
                    attacked_by="machine@fluidattacks.com",
                    attacked_lines=30,
                    be_present=True,
                    be_present_until=None,
                    comments="",
                    first_attack_at=datetime.fromisoformat(
                        "2020-02-19T15:41:04+00:00"
                    ),
                    has_vulnerabilities=False,
                    last_author="customer2@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c5",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    loc=180,
                    modified_by="machine@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-02-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=-1,
                ),
            ),
            ToeLines(
                filename="nickname/back/src/model/new_finding/index.js",
                group_name="group1",
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                state=ToeLinesState(
                    attacked_at=None,
                    attacked_by="machine@fluidattacks.com",
                    attacked_lines=23,
                    be_present=True,
                    be_present_until=None,
                    comments="",
                    first_attack_at=None,
                    has_vulnerabilities=False,
                    last_author="customer1@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-16T15:41:04+00:00"
                    ),
                    loc=4324,
                    modified_by="machine@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-16T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-01-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=0,
                ),
            ),
            ToeLines(
                filename="back/src/new_finding.js",
                group_name="group1",
                root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                state=ToeLinesState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-20T05:00:00+00:00"
                    ),
                    attacked_by="machine@fluidattacks.com",
                    attacked_lines=4,
                    be_present=True,
                    be_present_until=None,
                    comments="comment 2",
                    first_attack_at=datetime.fromisoformat(
                        "2020-02-19T15:41:04+00:00"
                    ),
                    has_vulnerabilities=False,
                    last_author="customer2@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    loc=180,
                    modified_by="machine@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-02-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=-1,
                ),
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
