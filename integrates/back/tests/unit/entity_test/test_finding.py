from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.tests.unit import (
    MIGRATION,
)
from back.tests.unit.utils import (
    create_dummy_session,
)
from custom_exceptions import (
    FindingNotFound,
    NotSubmitted,
)
from dataloaders import (
    apply_context_attrs,
    Dataloaders,
    get_new_context,
)
from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
)
from findings import (
    dal as findings_dal,
)
from findings.domain import (
    get_finding,
)
from freezegun import (
    freeze_time,
)
from groups.domain import (
    get_open_vulnerabilities,
    get_open_vulnerabilities_new,
)
import json
import os
import pytest
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    Dict,
    Optional,
)

pytestmark = pytest.mark.asyncio


async def _get_result(
    data: Dict[str, Any],
    user: str = "integratesmanager@gmail.com",
    loaders: Optional[Dataloaders] = None,
) -> Dict[str, Any]:
    """Get result."""
    request = await create_dummy_session(username=user)
    request = apply_context_attrs(request, loaders or get_new_context())
    _, result = await graphql(SCHEMA, data, context_value=request)
    return result


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
@freeze_time("2020-12-01")
async def test_finding_age() -> None:
    """Check for finding age."""
    query = """{
      finding(identifier: "422286126"){
          age
          lastVulnerability
          openAge
      }
    }"""
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert result["data"]["finding"]["age"] == 332
    assert result["data"]["finding"]["lastVulnerability"] == 332
    assert result["data"]["finding"]["openAge"] == 332


@pytest.mark.skipif(not MIGRATION, reason="Finding migration")
async def test_finding_age_new() -> None:
    """Check for finding age."""
    query = """{
      finding(identifier: "422286126"){
          age
          lastVulnerability
          openAge
      }
    }"""
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert result["data"]["finding"]["age"] == 613
    assert result["data"]["finding"]["lastVulnerability"] == 613
    assert result["data"]["finding"]["openAge"] == 613


async def test_finding() -> None:  # pylint: disable=too-many-statements
    """Check for finding query."""
    expected_vuln = {
        "id": "0a848781-b6a4-422e-95fa-692151e6a98z",
        "findingId": "422286126",
        "where": "test/data/lib_path/f060/csharp.cs",
        "specific": "12",
        "historicState": [
            {
                "analyst": "unittest@fluidattacks.com",
                "date": "2020-01-03 12:46:10",
                "source": "integrates",
                "state": "open",
            }
        ],
        "tag": "",
        "severity": "",
        "remediated": False,
        "verification": "",
        "historicVerification": [{"date": None, "status": None}],
        "historicZeroRisk": [{"date": None, "status": None}],
        "currentState": "open",
        "currentApprovalStatus": "",
        "hacker": "unittest@fluidattacks.com",
        "source": "asm",
        "vulnerabilityType": "lines",
        "zeroRisk": "",
    }
    expected_tracking = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "justification": "",
            "date": "2020-01-03",
            "accepted": 0,
            "accepted_undefined": 0,
            "manager": "",
        }
    ]
    query = """{
      finding(identifier: "422286126"){
          id
          groupName
          releaseDate
          openVulnerabilities
          closedVulnerabilities
          tracking
          records
          severity
          cvssVersion
          evidence
          consulting {
              id
              content
          }
          observations {
              id
              content
          }
          state
          lastVulnerability
          historicState
          title
          description
          requirements
          attackVectorDescription
          threat
          recommendation
          affectedSystems
          compromisedAttributes
          compromisedRecords
          risk
          remediated
          type
          age
          isExploitable
          severityScore
          reportDate
          hacker
          currentState
          newRemediated
          verified
          vulnerabilities {
            id
            findingId
            where
            specific
            historicState
            tag
            severity
            remediated
            verification
            historicVerification {
              date
              status
            }
            historicZeroRisk {
              date
              status
            }
            currentState
            currentApprovalStatus
            hacker
            source
            vulnerabilityType
            zeroRisk
          }
          portsVulnerabilities {
              specific
          }
          inputsVulnerabilities {
              specific
          }
          linesVulnerabilities {
              specific
          }
          __typename
      }
    }"""
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert result["data"]["finding"]["id"] == "422286126"
    assert result["data"]["finding"]["groupName"] == "unittesting"
    assert result["data"]["finding"]["openVulnerabilities"] == 1
    assert result["data"]["finding"]["closedVulnerabilities"] == 0
    assert result["data"]["finding"]["releaseDate"] == "2018-07-09 00:00:00"
    assert result["data"]["finding"]["tracking"] == expected_tracking
    assert "records" in result["data"]["finding"]
    assert result["data"]["finding"]["severity"]["attackComplexity"] == 0.77
    assert result["data"]["finding"]["severity"]["remediationLevel"] == 0.97
    assert result["data"]["finding"]["cvssVersion"] == "3.1"
    assert "evidence" in result["data"]["finding"]
    assert "evidence1" in result["data"]["finding"]["evidence"]
    assert "consulting" in result["data"]["finding"]
    assert (
        result["data"]["finding"]["consulting"][0]["content"]
        == "This is a comenting test"
    )
    assert "historicState" in result["data"]["finding"]
    assert "title" in result["data"]["finding"]
    assert "description" in result["data"]["finding"]
    assert "requirements" in result["data"]["finding"]
    assert "attackVectorDescription" in result["data"]["finding"]
    assert "threat" in result["data"]["finding"]
    assert "recommendation" in result["data"]["finding"]
    assert "affectedSystems" in result["data"]["finding"]
    assert "compromisedAttributes" in result["data"]["finding"]
    assert "compromisedRecords" in result["data"]["finding"]
    assert "risk" in result["data"]["finding"]
    assert "remediated" in result["data"]["finding"]
    assert "type" in result["data"]["finding"]
    assert "age" in result["data"]["finding"]
    assert "isExploitable" in result["data"]["finding"]
    assert "severityScore" in result["data"]["finding"]
    assert "reportDate" in result["data"]["finding"]
    assert "hacker" in result["data"]["finding"]
    assert "currentState" in result["data"]["finding"]
    assert "newRemediated" in result["data"]["finding"]
    assert "verified" in result["data"]["finding"]
    assert "observations" in result["data"]["finding"]
    assert result["data"]["finding"]["state"] == "open"
    assert "lastVulnerability" in result["data"]["finding"]
    assert "historicState" in result["data"]["finding"]
    assert "vulnerabilities" in result["data"]["finding"]
    assert result["data"]["finding"]["vulnerabilities"][-1] == expected_vuln
    for field, value in result["data"]["finding"]["vulnerabilities"][
        -1
    ].items():
        assert value == expected_vuln[field]


@pytest.mark.changes_db
async def test_remove_evidence() -> None:
    """Check for removeEvidence mutation."""
    query = """
      mutation RemoveEvidenceMutation(
        $evidenceId: EvidenceType!,
        $findingId: String!
      ) {
        removeEvidence(evidenceId: $evidenceId, findingId: $findingId) {
        success
        }
      }
    """
    variables = {"evidenceId": "EVIDENCE2", "findingId": "457497316"}
    data = {"query": query, "variables": variables}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["removeEvidence"]


@pytest.mark.changes_db
async def test_update_evidence() -> None:
    """Check for updateEvidence mutation."""
    query = """
      mutation UpdateEvidenceMutation(
        $evidenceId: EvidenceType!, $file: Upload!, $findingId: String!
      ) {
        updateEvidence(
          evidenceId: $evidenceId, file: $file, findingId: $findingId
        ) {
          success
        }
      }
    """
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-anim.gif")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, "image/gif")
        variables = {
            "evidenceId": "ANIMATION",
            "findingId": "422286126",
            "file": uploaded_file,
        }
        data = {"query": query, "variables": variables}
        result = await _get_result(data)

    assert "errors" not in result
    assert "success" in result["data"]["updateEvidence"]
    assert result["data"]["updateEvidence"]["success"]


@pytest.mark.changes_db
async def test_update_evidence_records_append() -> None:
    number_of_records = 4
    query = """
      query GetFindingRecords($findingId: String!) {
        finding(identifier: $findingId) {
          records
          id
        }
      }
    """
    data = {"query": query, "variables": {"findingId": "422286126"}}
    result = await _get_result(data)
    assert "errors" not in result
    assert (
        len(json.loads(result["data"]["finding"]["records"]))
        == number_of_records
    )

    mutation = """
      mutation UpdateEvidenceMutation(
        $evidenceId: EvidenceType!, $file: Upload!, $findingId: String!
      ) {
        updateEvidence(
          evidenceId: $evidenceId, file: $file, findingId: $findingId
        ) {
          success
        }
      }
    """
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "../mock/test-file-records.csv")
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, "text/csv")
        variables = {
            "evidenceId": "RECORDS",
            "findingId": "422286126",
            "file": uploaded_file,
        }
        data = {"query": mutation, "variables": variables}
        result = await _get_result(data)

    assert "errors" not in result
    assert "success" in result["data"]["updateEvidence"]
    assert result["data"]["updateEvidence"]["success"]

    data = {"query": query, "variables": {"findingId": "422286126"}}
    result = await _get_result(data)
    assert "errors" not in result
    assert (
        len(json.loads(result["data"]["finding"]["records"]))
        > number_of_records
    )


@pytest.mark.changes_db
async def test_update_evidence_description() -> None:
    """Check for updateEvidenceDescription mutation."""
    query = """
        mutation {
            updateEvidenceDescription(
            description: "this is a test description",
            findingId: "422286126",
            evidenceId: EVIDENCE2) {
            success
            }
        }
    """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["updateEvidenceDescription"]
    assert result["data"]["updateEvidenceDescription"]


@pytest.mark.changes_db
async def test_update_severity() -> None:
    """Check for updateSeverity mutation."""
    query = """
            mutation {
              updateSeverity (
                findingId: "422286126",
                attackComplexity: "0.77", attackVector: "0.62",
                availabilityImpact: "0", availabilityRequirement: "1",
                confidentialityImpact: "0", confidentialityRequirement: "1",
                cvssVersion: "3.1", exploitability: "0.91",
                integrityImpact: "0.22", integrityRequirement: "1",
                modifiedAttackComplexity: "0.77", modifiedAttackVector: "0.62",
                modifiedAvailabilityImpact: "0",
                modifiedConfidentialityImpact: "0",
                modifiedIntegrityImpact: "0.22",
                modifiedPrivilegesRequired: "0.62",
                modifiedSeverityScope: "0", modifiedUserInteraction: "0.85",
                privilegesRequired: "0.62", remediationLevel: "0.97",
                reportConfidence: "0.92",
                severity: "2.9", severityScope: "0", userInteraction: "0.85"
              ) {
                success
                finding {
                  cvssVersion
                  severity
                }
              }
            }
    """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["updateSeverity"]
    assert result["data"]["updateSeverity"]["success"]


@pytest.mark.changes_db
async def test_add_finding_consult_parent_zero() -> None:
    """Check for addFindingConsult mutation."""
    query = """
      mutation {
        addFindingConsult(
          content: "This is a comenting test",
          findingId: "422286126",
          type: CONSULT,
          parent: "0"
        ) {
          success
          commentId
        }
      }
      """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["addFindingConsult"]
    assert result["data"]["addFindingConsult"]["success"]


@pytest.mark.changes_db
async def test_add_finding_consult_parent_non_zero() -> None:
    """Check for addFindingConsult mutation."""
    query = """
      mutation {
        addFindingConsult(
          content: "This is a comenting test",
          findingId: "422286126",
          type: CONSULT,
          parent: "1566336916294"
        ) {
          success
          commentId
        }
      }
      """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["addFindingConsult"]
    assert result["data"]["addFindingConsult"]["success"]


@pytest.mark.changes_db
async def test_update_description() -> None:
    """Check for updateDescription mutation."""
    query = """
        mutation UpdateFindingDescription(
            $affectedSystems: String!,
            $attackVectorDescription: String!,
            $compromisedAttributes: String,
            $compromisedRecords: Int!,
            $description: String!,
            $findingId: String!,
            $recommendation: String!,
            $threat: String!,
            $type: String
        ){
            updateDescription(
            affectedSystems: $affectedSystems,
            attackVectorDescription: $attackVectorDescription,
            description: $description,
            findingId: $findingId,
            records: $compromisedAttributes,
            recommendation: $recommendation,
            recordsNumber: $compromisedRecords,
            threat: $threat,
            findingType: $type
            ) {
            success
            }
        }
    """
    variables = {
        "affectedSystems": "Server bWAPP",
        "attackVectorDescription": "This is an updated attack vector",
        "compromisedAttributes": "Clave plana",
        "compromisedRecords": 12,
        "description": "I just have updated the description",
        "findingId": "422286126",
        "recommendation": "Updated recommendation",
        "threat": "Updated threat",
        "type": "SECURITY",
    }
    data = {"query": query, "variables": variables}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["updateDescription"]
    assert result["data"]["updateDescription"]["success"]


@pytest.mark.changes_db
async def test_reject_draft() -> None:
    """Check for rejectDraft mutation."""
    query = """
        mutation {
            rejectDraft(findingId: "836530833") {
                success
            }
        }
    """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["rejectDraft"]
    assert result["data"]["rejectDraft"]


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
@pytest.mark.changes_db
async def test_remove_finding() -> None:
    """Check for removeFinding mutation."""
    query = """
      mutation {
        removeFinding(findingId: "560175507", justification: NOT_REQUIRED) {
          success
        }
      }
    """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["removeFinding"]
    assert result["data"]["removeFinding"]["success"]
    finding = await findings_dal.get_finding("560175507")
    historic_state = finding["historic_state"]
    assert historic_state[-1]["state"] == "DELETED"
    assert historic_state[-1]["justification"] == "NOT_REQUIRED"
    with pytest.raises(FindingNotFound):
        assert await get_finding("560175507")


@pytest.mark.skipif(not MIGRATION, reason="Finding migration")
@pytest.mark.changes_db
async def test_remove_finding_new() -> None:
    """Check for removeFinding mutation."""
    finding_id = "560175507"
    loaders: Dataloaders = get_new_context()
    finding: Finding = await loaders.finding_new.load(finding_id)
    assert finding.state.status == FindingStateStatus.CREATED

    query = f"""
      mutation {{
        removeFinding(
          findingId: "{finding_id}"
          justification: NOT_REQUIRED
        ) {{
          success
        }}
      }}
    """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["removeFinding"]
    assert result["data"]["removeFinding"]["success"]

    loaders.finding_new.clear(finding_id)
    with pytest.raises(FindingNotFound):
        assert await loaders.finding_new.load(finding_id)


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
@pytest.mark.changes_db
async def test_approve_draft() -> None:
    """Check for approveDraft mutation."""
    query = """
      mutation {
        approveDraft(draftId: "836530833") {
          success
        }
      }
    """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" in result
    assert (
        result["errors"][0]["message"] == "CANT_APPROVE_FINDING_WITHOUT_VULNS"
    )


@pytest.mark.skipif(not MIGRATION, reason="Finding migration")
@pytest.mark.changes_db
async def test_approve_draft_new() -> None:
    """Check for approveDraft mutation."""
    query = """
      mutation {
        approveDraft(draftId: "836530833") {
          success
        }
      }
    """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" in result
    assert result["errors"][0]["message"] == str(NotSubmitted())


@pytest.mark.changes_db
async def test_create_draft() -> None:
    """Check for addDraft mutation."""
    query = """
        mutation AddDraftMutation(
            $description: String,
            $groupName: String!,
            $recommendation: String,
            $requirements: String,
            $risk: String,
            $threat: String,
            $title: String!,
            $type: FindingType
            ) {
            addDraft(
            description: $description,
            groupName: $groupName,
            recommendation: $recommendation,
            requirements: $requirements,
            risk: $risk,
            threat: $threat,
            title: $title,
            type: $type
            ) {
            success
            }
        }
    """
    variables = {
        "description": "This is pytest created draft",
        "groupName": "UNITTESTING",
        "recommendation": "Solve this finding",
        "requirements": "REQ.0001. Apply filters",
        "risk": "Losing money",
        "threat": "Attacker",
        "title": "001. SQL injection - C Sharp SQL API",
        "type": "SECURITY",
    }
    data = {"query": query, "variables": variables}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["addDraft"]
    assert result["data"]["addDraft"]["success"]


@pytest.mark.changes_db
async def test_submit_draft() -> None:
    """Check for submitDraft mutation."""
    query = """
      mutation {
        submitDraft(findingId: "475041535") {
          success
        }
      }
    """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" in result
    expected_error = (
        "Exception - This draft has missing fields: vulnerabilities"
    )
    assert result["errors"][0]["message"] == expected_error


@pytest.mark.skipif(MIGRATION, reason="Finding migration")
@pytest.mark.changes_db
async def test_filter_deleted_findings() -> None:
    """Check if vuln of removed vulns are filtered out."""
    mutation = """
      mutation {
        removeFinding(findingId: "988493279", justification: NOT_REQUIRED) {
          success
        }
      }
    """
    loaders: Dataloaders = get_new_context()
    open_vulns = await get_open_vulnerabilities(loaders, "unittesting")

    data = {"query": mutation}
    result = await _get_result(data, loaders=loaders)
    assert "errors" not in result
    assert "success" in result["data"]["removeFinding"]
    assert result["data"]["removeFinding"]["success"]
    assert await get_open_vulnerabilities(loaders, "unittesting") < open_vulns


@pytest.mark.skipif(not MIGRATION, reason="Finding migration")
@pytest.mark.changes_db
async def test_filter_deleted_findings_new() -> None:
    """Check if vulns of removed findings are filtered out"""
    finding_id = "988493279"
    group_name = "unittesting"
    mutation = f"""
      mutation {{
        removeFinding(
          findingId: "{finding_id}", justification: NOT_REQUIRED
        ) {{
          success
        }}
      }}
    """
    loaders: Dataloaders = get_new_context()
    open_vulns = await get_open_vulnerabilities_new(loaders, group_name)

    data = {"query": mutation}
    result = await _get_result(data, loaders=loaders)
    assert "errors" not in result
    assert "success" in result["data"]["removeFinding"]
    assert result["data"]["removeFinding"]["success"]
    loaders.group_findings_new.clear(group_name)
    loaders.group_findings_all_new.clear(group_name)
    assert await get_open_vulnerabilities_new(loaders, group_name) < open_vulns


async def test_non_existing_finding() -> None:
    query = """
      query GetFindingHeader($findingId: String!) {
        finding(identifier: $findingId) {
          closedVulns: closedVulnerabilities
          id
          openVulns: openVulnerabilities
          releaseDate
        }
      }
    """
    variables = {
        "findingId": "777493279",
    }
    data = {"query": query, "variables": variables}
    result = await _get_result(data)
    assert "errors" in result
    expected_error = "Access denied"
    assert result["errors"][0]["message"] == expected_error
