from back.tests.functional.group_manager.utils import (
    get_result,
)
from custom_exceptions import (
    UserNotInOrganization,
)
import json
from names.domain import (
    get_name,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("old")
async def test_group() -> None:  # pylint: disable=too-many-statements
    org_name = "okada"
    group_name = await get_name("group")
    query = f"""
        mutation {{
            createGroup(
                organization: "{org_name}",
                description: "This is a new group from pytest",
                groupName: "{group_name}",
                subscription: CONTINUOUS,
                hasMachine: true,
                hasSquad: true,
            ) {{
            success
            }}
        }}
    """
    data: Dict[str, Any] = {"query": query}
    result = await get_result(data, stakeholder="integratesmanager@gmail.com")
    assert "errors" not in result
    assert "success" in result["data"]["createGroup"]
    assert result["data"]["createGroup"]["success"]

    group_name2 = await get_name("group")
    query = f"""
        mutation {{
            createGroup(
                organization: "{org_name}",
                description: "This is a new group from pytest",
                groupName: "{group_name2}",
                subscription: CONTINUOUS,
                hasMachine: true,
                hasSquad: true,
            ) {{
            success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, stakeholder="integratesmanager@gmail.com")
    assert "errors" not in result
    assert "success" in result["data"]["createGroup"]
    assert result["data"]["createGroup"]["success"]

    role = "GROUP_MANAGER"
    groupmanager_email = "unittest2@fluidattacks.com"
    query = f"""
        mutation {{
            editStakeholder (
                email: "{groupmanager_email}",
                phoneNumber: "-",
                groupName: "{group_name}",
                responsibility: "Group manager",
                role: {role}
            ) {{
            success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, stakeholder="integratesmanager@gmail.com")
    assert "errors" not in result
    assert result["data"]["editStakeholder"]["success"]

    query = f"""
        mutation {{
            editStakeholder (
                email: "{groupmanager_email}",
                phoneNumber: "-",
                groupName: "{group_name2}",
                responsibility: "Group manager",
                role: {role}
            ) {{
            success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, stakeholder="integratesmanager@gmail.com")
    assert "errors" not in result
    assert result["data"]["editStakeholder"]["success"]

    query = f"""
        mutation {{
            removeGroup(
                groupName: "{group_name2}"
            ) {{
            success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["removeGroup"]
    assert result["data"]["removeGroup"]["success"]

    query = f"""
        mutation {{
            addGroupConsult(
                content: "Test consult",
                parent: "0",
                groupName: "{group_name}",
            ) {{
                success
                commentId
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["addGroupConsult"]
    assert result["data"]["addGroupConsult"]["success"]

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
    result = await get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["addTags"]
    assert result["data"]["addTags"]["success"]

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
                drafts {{
                    age
                }}
                events {{
                    analyst
                    detail
                }}
                stakeholders {{
                    email
                    role
                }}
                serviceAttributes
                bill{{
                    authors{{
                        actor
                    }}
                }}
                __typename
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data)
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
        {"content": "Test consult"}
    ]
    assert result["data"]["group"]["drafts"] == []
    assert result["data"]["group"]["events"] == []
    assert {
        "email": "unittest2@fluidattacks.com",
        "role": "group_manager",
    } in result["data"]["group"]["stakeholders"]
    assert {
        "email": f"forces.{group_name}@fluidattacks.com",
        "role": "service_forces",
    } in result["data"]["group"]["stakeholders"]
    assert result["data"]["group"]["serviceAttributes"] == [
        "has_drills_white",
        "has_forces",
        "has_integrates",
        "has_squad",
        "is_continuous",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    ]
    assert result["data"]["group"]["bill"] == {"authors": []}

    query = f"""
        query {{
            group(groupName: "{group_name}"){{
                findings(
                    filters: {{
                        affectedSystems: "test",
                        actor: "ANY_EMPLOYEE"
                    }}
                ) {{
                id
                }}
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data)
    assert "errors" not in result
    assert result["data"]["group"]["findings"] == []

    query = f"""
        query {{
            group(groupName: "{group_name}"){{
                findings(filters: {{affectedSystems: "notexists"}}) {{
                    id
                }}
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data)
    assert "errors" not in result
    assert result["data"]["group"]["findings"] == []

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
    result = await get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["removeTag"]
    assert result["data"]["removeTag"]["success"]

    query = f"""
        query {{
            group(groupName: "{group_name}"){{
                tags
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data)
    assert "errors" not in result
    assert result["data"]["group"]["tags"] == []

    query = f"""
      mutation {{
        addGitRoot(
          branch: "master"
          environment: "production"
          gitignore: []
          groupName: "{group_name}"
          includesHealthCheck: true
          url: "https://gitlab.com/fluidattacks/test5"
        ) {{
          success
        }}
      }}
    """
    result = await get_result({"query": query})
    assert "errors" not in result
    assert result["data"]["addGitRoot"]["success"]

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
    result = await get_result({"query": query})
    assert "errors" not in result
    assert {
        "__typename": "GitRoot",
        "branch": "master",
        "environment": "production",
        "environmentUrls": [],
        "gitignore": [],
        "includesHealthCheck": True,
        "url": "https://gitlab.com/fluidattacks/test5",
    } in result["data"]["group"]["roots"]

    query = f"""
        mutation {{
            editGroup(
                comments: "",
                groupName: "{group_name}",
                subscription: ONESHOT,
                hasSquad: false,
                hasAsm: false,
                hasMachine: false,
                reason: NONE,
            ) {{
                success
            }}
        }}
      """
    data = {"query": query}
    result = await get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["editGroup"]
    assert result["data"]["editGroup"]["success"]

    query = f"""
        query {{
            group(groupName: "{group_name}"){{
                hasSquad
                hasForces
                hasAsm
                subscription
                __typename
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data)
    assert "errors" in result
    assert result["errors"][0]["message"] == str(UserNotInOrganization())
