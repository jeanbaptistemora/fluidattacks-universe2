# Standard libraries
import json
import os
import pytest
from typing import (
    Any,
    Dict,
    Optional,
)

# Third party libraries
from ariadne import graphql
from freezegun import freeze_time
from starlette.datastructures import UploadFile

# Local libraries
from api.schema import SCHEMA
from back.tests.unit.utils import create_dummy_session
from custom_exceptions import FindingNotFound
from dataloaders import (
    Dataloaders,
    apply_context_attrs,
    get_new_context,
)
from findings import dal as findings_dal
from findings.domain import get_finding
from groups.domain import get_open_vulnerabilities


pytestmark = pytest.mark.asyncio


async def _get_result(
    data: Dict[str, Any],
    user: str = "integratesmanager@gmail.com",
    context: Optional[Dataloaders] = None,
) -> Dict[str, Any]:
    """Get result."""
    request = await create_dummy_session(username=user)
    request = apply_context_attrs(
        request, loaders=context if context else get_new_context()
    )
    _, result = await graphql(SCHEMA, data, context_value=request)
    return result


@freeze_time("2020-12-01")
async def test_finding_age():
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


async def test_finding():
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
        "analyst": "unittest@fluidattacks.com",
        "source": "integrates",
        "vulnType": "lines",
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
          projectName
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
          scenario
          actor
          description
          requirements
          attackVectorDesc
          threat
          recommendation
          affectedSystems
          compromisedAttributes
          compromisedRecords
          cweUrl
          btsUrl
          risk
          remediated
          type
          age
          isExploitable
          severityScore
          reportDate
          analyst
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
            analyst
            source
            vulnType
            zeroRisk
          }
          portsVulns {
              specific
          }
          inputsVulns {
              specific
          }
          linesVulns {
              specific
          }
          __typename
      }
    }"""
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert result["data"]["finding"]["id"] == "422286126"
    assert result["data"]["finding"]["projectName"] == "unittesting"
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
    assert "scenario" in result["data"]["finding"]
    assert "actor" in result["data"]["finding"]
    assert "description" in result["data"]["finding"]
    assert "requirements" in result["data"]["finding"]
    assert "attackVectorDesc" in result["data"]["finding"]
    assert "threat" in result["data"]["finding"]
    assert "recommendation" in result["data"]["finding"]
    assert "affectedSystems" in result["data"]["finding"]
    assert "compromisedAttributes" in result["data"]["finding"]
    assert "compromisedRecords" in result["data"]["finding"]
    assert "cweUrl" in result["data"]["finding"]
    assert "btsUrl" in result["data"]["finding"]
    assert "risk" in result["data"]["finding"]
    assert "remediated" in result["data"]["finding"]
    assert "type" in result["data"]["finding"]
    assert "age" in result["data"]["finding"]
    assert "isExploitable" in result["data"]["finding"]
    assert "severityScore" in result["data"]["finding"]
    assert "reportDate" in result["data"]["finding"]
    assert "analyst" in result["data"]["finding"]
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
async def test_remove_evidence():
    """Check for removeEvidence mutation."""
    query = """
        mutation RemoveEvidenceMutation($evidenceId: EvidenceType!, $findingId: String!) {
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
async def test_update_evidence():
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
async def test_update_evidence_records_append():
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
async def test_update_evidence_description():
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
async def test_update_severity():
    """Check for updateSeverity mutation."""
    query = """
            mutation {
              updateSeverity (
                findingId: "422286126",
                data: {
        attackComplexity: 0.77, attackVector: 0.62,
        availabilityImpact: "0", availabilityRequirement: "1",
        confidentialityImpact: "0", confidentialityRequirement: "1",
        cvssVersion: "3.1", exploitability: 0.91, id: "422286126",
        integrityImpact: "0.22", integrityRequirement: "1",
        modifiedAttackComplexity: 0.77, modifiedAttackVector: 0.62,
        modifiedAvailabilityImpact: "0",
        modifiedConfidentialityImpact: "0",
        modifiedIntegrityImpact: "0.22",
        modifiedPrivilegesRequired: "0.62",
        modifiedSeverityScope: 0, modifiedUserInteraction: 0.85,
        privilegesRequired: "0.62", remediationLevel: "0.97",
        reportConfidence: "0.92",
        severity: "2.9", severityScope: 0, userInteraction: 0.85
                }
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
async def test_add_finding_consult_parent_zero():
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
async def test_add_finding_consult_parent_non_zero():
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
async def test_update_description():
    """Check for updateDescription mutation."""
    query = """
        mutation UpdateFindingDescription(
            $actor: String!,
            $affectedSystems: String!,
            $attackVectorDesc: String!,
            $compromisedAttributes: String,
            $compromisedRecords: Int!,
            $cweUrl: String!,
            $description: String!,
            $findingId: String!,
            $recommendation: String!,
            $requirements: String!,
            $scenario: String!,
            $threat: String!,
            $title: String!,
            $type: String
        ){
            updateDescription(
            actor: $actor,
            affectedSystems: $affectedSystems,
            attackVectorDesc: $attackVectorDesc,
            cwe: $cweUrl,
            description: $description,
            findingId: $findingId,
            records: $compromisedAttributes,
            recommendation: $recommendation,
            recordsNumber: $compromisedRecords,
            requirements: $requirements,
            scenario: $scenario,
            threat: $threat,
            title: $title,
            findingType: $type
            ) {
            success
            }
        }
    """
    variables = {
        "actor": "ANYONE_INTERNET",
        "affectedSystems": "Server bWAPP",
        "attackVectorDesc": "This is an updated attack vector",
        "compromisedAttributes": "Clave plana",
        "compromisedRecords": 12,
        "cweUrl": "200",
        "description": "I just have updated the description",
        "findingId": "422286126",
        "recommendation": "Updated recommendation",
        "requirements": "REQ.0132. Passwords (phrase type) must be at least 3 words long.",
        "scenario": "UNAUTHORIZED_USER_EXTRANET",
        "threat": "Updated threat",
        "title": "F051. Weak passwords reversed",
        "type": "SECURITY",
    }
    data = {"query": query, "variables": variables}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["updateDescription"]
    assert result["data"]["updateDescription"]["success"]


@pytest.mark.changes_db
async def test_reject_draft():
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


@pytest.mark.changes_db
@freeze_time("2020-12-01")
async def test_delete_finding():
    """Check for deleteFinding mutation."""
    query = """
      mutation {
        deleteFinding(findingId: "560175507", justification: NOT_REQUIRED) {
          success
        }
      }
    """
    data = {"query": query}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["deleteFinding"]
    assert result["data"]["deleteFinding"]["success"]
    finding = await findings_dal.get_finding("560175507")
    historic_state = finding["historic_state"]
    assert historic_state == [
        {
            "analyst": "unittest@fluidattacks.com",
            "date": "2019-02-04 12:46:10",
            "source": "integrates",
            "state": "CREATED",
        },
        {
            "analyst": "integratesmanager@gmail.com",
            "date": "2020-11-30 19:00:00",
            "justification": "NOT_REQUIRED",
            "source": "integrates",
            "state": "DELETED",
        },
    ]
    with pytest.raises(FindingNotFound):
        assert await get_finding("560175507")


@pytest.mark.changes_db
async def test_approve_draft():
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


@pytest.mark.changes_db
async def test_create_draft():
    """Check for createDraft mutation."""
    query = """
        mutation CreateDraftMutation(
            $cwe: String,
            $description: String,
            $projectName: String!,
            $recommendation: String,
            $requirements: String,
            $risk: String,
            $threat: String,
            $title: String!,
            $type: FindingType
            ) {
            createDraft(
            cwe: $cwe,
            description: $description,
            projectName: $projectName,
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
        "cwe": "200",
        "description": "This is pytest created draft",
        "projectName": "UNITTESTING",
        "recommendation": "Solve this finding",
        "requirements": "REQ.0001. Apply filters",
        "risk": "Losing money",
        "threat": "Attacker",
        "title": "F001. Very serious vulnerability",
        "type": "SECURITY",
    }
    data = {"query": query, "variables": variables}
    result = await _get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["createDraft"]
    assert result["data"]["createDraft"]["success"]


@pytest.mark.changes_db
async def test_submit_draft():
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


@pytest.mark.changes_db
async def test_filter_deleted_findings():
    """Check if vuln of deleted vulns are filter out."""
    mutation = """
      mutation {
        deleteFinding(findingId: "988493279", justification: NOT_REQUIRED) {
          success
        }
      }
    """
    context = get_new_context()
    open_vulns = await get_open_vulnerabilities(context, "unittesting")

    data = {"query": mutation}
    result = await _get_result(data, context=context)
    assert "errors" not in result
    assert "success" in result["data"]["deleteFinding"]
    assert result["data"]["deleteFinding"]["success"]
    assert await get_open_vulnerabilities(context, "unittesting") < open_vulns


async def test_non_existing_finding():
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
