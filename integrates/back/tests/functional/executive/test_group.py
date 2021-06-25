from back.tests.functional.executive.utils import (
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
async def test_group() -> None:  # pylint: disable=too-many-statements
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
    role = "EXECUTIVE"
    executive_email = "integratesexecutive@gmail.com"
    query = f"""
        mutation {{
            grantStakeholderAccess (
                email: "{executive_email}",
                phoneNumber: "-",
                groupName: "{group_name}",
                responsibility: "Executive",
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
    assert await complete_register(executive_email, group_name)

    context = get_new_context()
    consult_content = "Test consult"
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
    assert "errors" not in result
    assert "success" in result["data"]["addTags"]
    assert result["data"]["addTags"]["success"]

    context = get_new_context()
    query = f"""
        query {{
            group(groupName: "{group_name}"){{
                name
                hasSquad
                hasForces
                findings {{
                    analyst
                }}
                hasAsm
                openVulnerabilities
                closedVulnerabilities
                lastClosingVuln
                maxSeverity
                meanRemediate
                meanRemediateLowSeverity
                meanRemediateMediumSeverity
                openFindings
                totalFindings
                totalTreatment
                subscription
                deletionDate
                userDeletion
                tags
                description
                consulting {{
                    content
                }}
                events {{
                    analyst
                    detail
                }}
                serviceAttributes
                __typename
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" not in result
    assert result["data"]["group"]["name"] == group_name
    assert result["data"]["group"]["hasSquad"]
    assert result["data"]["group"]["hasForces"]
    assert result["data"]["group"]["hasAsm"]
    assert result["data"]["group"]["findings"] == []
    assert result["data"]["group"]["openVulnerabilities"] == 0
    assert result["data"]["group"]["closedVulnerabilities"] == 0
    assert result["data"]["group"]["lastClosingVuln"] == 0
    assert result["data"]["group"]["maxSeverity"] == 0.0
    assert result["data"]["group"]["meanRemediate"] == 0
    assert result["data"]["group"]["meanRemediateLowSeverity"] == 0
    assert result["data"]["group"]["meanRemediateMediumSeverity"] == 0
    assert result["data"]["group"]["openFindings"] == 0
    assert result["data"]["group"]["totalFindings"] == 0
    assert result["data"]["group"]["totalTreatment"] == "{}"
    assert result["data"]["group"]["subscription"] == "continuous"
    assert result["data"]["group"]["deletionDate"] == ""
    assert result["data"]["group"]["userDeletion"] == ""
    assert result["data"]["group"]["tags"] == ["testing"]
    assert (
        result["data"]["group"]["description"]
        == "This is a new group from pytest"
    )
    assert result["data"]["group"]["consulting"] == [
        {"content": consult_content}
    ]
    assert result["data"]["group"]["events"] == []
    assert result["data"]["group"]["serviceAttributes"] == [
        "has_drills_white",
        "has_forces",
        "has_integrates",
        "is_continuous",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    ]

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
    assert "errors" not in result
    assert "success" in result["data"]["removeTag"]
    assert result["data"]["removeTag"]["success"]

    context = get_new_context()
    query = f"""
        query {{
            group(groupName: "{group_name}"){{
                tags
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" not in result
    assert result["data"]["group"]["tags"] == []

    context = get_new_context()
    query = f"""
      mutation {{
        addGitRoot(
          branch: "master"
          environment: "production"
          gitignore: []
          groupName: "{group_name}"
          includesHealthCheck: true
          url: "https://gitlab.com/fluidattacks/test4"
        ) {{
          success
        }}
      }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" not in result
    assert result["data"]["addGitRoot"]["success"]

    context = get_new_context()
    query = f"""
        query {{
          group(groupName: "{group_name}") {{
            roots {{
              __typename
              ...on GitRoot {{
                branch
                environment
                environmentUrls
                gitignore
                includesHealthCheck
                url
              }}
            }}
          }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" not in result
    assert {
        "__typename": "GitRoot",
        "branch": "master",
        "environment": "production",
        "environmentUrls": [],
        "gitignore": [],
        "includesHealthCheck": True,
        "url": "https://gitlab.com/fluidattacks/test4",
    } in result["data"]["group"]["roots"]

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
