from back.tests.functional.reviewer.utils import (
    get_result,
)
from back.tests.functional.utils import (
    complete_register,
)
from dataloaders import (
    get_new_context,
)
import json
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("old")
async def test_group() -> None:
    context = get_new_context()
    query = """{
        internalNames(entity: GROUP){
            name
            __typename
        }
    }"""
    data: Dict[str, Any] = {"query": query}
    result = await get_result(
        data, stakeholder="integratesmanager@gmail.com", context=context
    )
    assert "errors" not in result
    assert "internalNames" in result["data"]
    group_name = result["data"]["internalNames"]["name"]

    context = get_new_context()
    org_name = "okada"
    query = f"""
        mutation {{
            createGroup(
                organization: "{org_name}",
                description: "This is a new group from pytest",
                groupName: "{group_name}",
                subscription: CONTINUOUS,
                hasMachine: true,
                hasSquad: true,
                hasForces: true
            ) {{
            success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(
        data, stakeholder="integratesmanager@gmail.com", context=context
    )
    assert "errors" not in result
    assert "success" in result["data"]["createGroup"]
    assert result["data"]["createGroup"]["success"]

    context = get_new_context()
    role = "REVIEWER"
    reviewer_email = "integratesreviewer@fluidattacks.com"
    query = f"""
        mutation {{
            grantStakeholderAccess (
                email: "{reviewer_email}",
                phoneNumber: "-",
                groupName: "{group_name}",
                responsibility: "Resourcer",
                role: {role}
            ) {{
            success
                grantedStakeholder {{
                    email
                }}
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(
        data, stakeholder="integratesmanager@gmail.com", context=context
    )
    assert "errors" not in result
    assert result["data"]["grantStakeholderAccess"]["success"]
    assert await complete_register(reviewer_email, group_name)

    context = get_new_context()
    consult_content = "Test reviewer consult"
    query = f"""
        mutation {{
            addGroupConsult(
                content: "{consult_content}",
                parent: "0",
                groupName: "{group_name}",
            ) {{
                success
                commentId
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" not in result
    assert "success" in result["data"]["addGroupConsult"]
    assert result["data"]["addGroupConsult"]["success"]

    context = get_new_context()
    query = """
        mutation AddTagsMutation(
            $groupName: String!,
            $tagsData: JSONString!
        ) {
            addTags (
                tags: $tagsData,
                groupName: $groupName) {
                success
            }
        }
    """
    variables = {
        "groupName": group_name,
        "tagsData": json.dumps(["testing"]),
    }
    data = {"query": query, "variables": variables}
    result = await get_result(data, context=context)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    context = get_new_context()
    query = f"""
        mutation {{
            removeTag (
                tag: "testing",
                groupName: "{group_name}",
            ) {{
                success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    context = get_new_context()
    query = f"""
        mutation {{
            editGroup(
                comments: "",
                groupName: "{group_name}",
                subscription: ONESHOT,
                hasSquad: false,
                hasForces: false,
                hasAsm: false,
                hasMachine: false,
                reason: NONE,
            ) {{
                success
            }}
        }}
      """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"

    context = get_new_context()
    query = f"""
        query {{
            group(groupName: "{group_name}"){{
                analytics(documentName: "", documentType: "")
                closedVulnerabilities
                consulting {{
                    content
                }}
                drafts {{
                    analyst
                }}
                deletionDate
                description
                events {{
                    analyst
                    detail
                }}
                findings {{
                    analyst
                }}
                hasSquad
                hasForces
                hasAsm
                lastClosingVuln
                lastClosingVulnFinding {{
                    analyst
                }}
                maxOpenSeverity
                maxOpenSeverityFinding {{
                    analyst
                }}
                maxSeverity
                maxSeverityFinding {{
                    analyst
                }}
                meanRemediate
                meanRemediateCriticalSeverity
                meanRemediateHighSeverity
                meanRemediateLowSeverity
                meanRemediateMediumSeverity
                name
                openFindings
                openVulnerabilities
                organization
                serviceAttributes
                stakeholders {{
                    email
                    firstLogin
                    lastLogin
                    phoneNumber
                    responsibility
                    role
                }}
                subscription
                tags
                totalFindings
                totalTreatment
                userDeletion
                userRole
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" in result
    assert len(result["errors"]) == 1
    assert result["errors"][0]["message"] == "Exception - Document not found"
    assert result["data"]["group"]["closedVulnerabilities"] == 0
    assert result["data"]["group"]["consulting"] == [
        {"content": consult_content}
    ]
    assert result["data"]["group"]["drafts"] == []
    assert result["data"]["group"]["deletionDate"] == ""
    assert (
        result["data"]["group"]["description"]
        == "This is a new group from pytest"
    )
    assert result["data"]["group"]["events"] == []
    assert result["data"]["group"]["findings"] == []
    assert result["data"]["group"]["hasSquad"]
    assert result["data"]["group"]["hasForces"]
    assert result["data"]["group"]["hasAsm"]
    assert result["data"]["group"]["lastClosingVuln"] == 0
    assert result["data"]["group"]["lastClosingVulnFinding"] is None
    assert result["data"]["group"]["maxOpenSeverity"] == 0.0
    assert result["data"]["group"]["maxOpenSeverityFinding"] is None
    assert result["data"]["group"]["maxSeverity"] == 0.0
    assert result["data"]["group"]["maxSeverityFinding"] is None
    assert result["data"]["group"]["meanRemediate"] == 0
    assert result["data"]["group"]["meanRemediateCriticalSeverity"] == 0
    assert result["data"]["group"]["meanRemediateHighSeverity"] == 0
    assert result["data"]["group"]["meanRemediateLowSeverity"] == 0
    assert result["data"]["group"]["meanRemediateMediumSeverity"] == 0
    assert result["data"]["group"]["name"] == group_name
    assert result["data"]["group"]["openFindings"] == 0
    assert result["data"]["group"]["openVulnerabilities"] == 0
    assert result["data"]["group"]["organization"] == org_name
    assert result["data"]["group"]["serviceAttributes"] == [
        "has_drills_white",
        "has_forces",
        "has_integrates",
        "is_continuous",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    ]
    assert len(result["data"]["group"]["stakeholders"]) == 3
    assert result["data"]["group"]["subscription"] == "continuous"
    assert result["data"]["group"]["tags"] == []
    assert result["data"]["group"]["totalFindings"] == 0
    assert result["data"]["group"]["totalTreatment"] == "{}"
    assert result["data"]["group"]["userDeletion"] == ""
    assert result["data"]["group"]["userRole"] == role.lower()

    context = get_new_context()
    query = f"""
        mutation {{
            unsubscribeFromGroup(groupName: "{group_name}"){{
                success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" not in result
    assert result["data"]["unsubscribeFromGroup"]["success"]

    context = get_new_context()
    query = f"""
        query {{
            group(groupName: "{group_name}"){{
                name
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
