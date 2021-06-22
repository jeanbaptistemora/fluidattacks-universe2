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
async def test_project() -> None:  # pylint: disable=too-many-statements
    org_name = "okada"
    group_name = await get_name("group")
    query = f"""
        mutation {{
            createProject(
                organization: "{org_name}",
                description: "This is a new project from pytest",
                projectName: "{group_name}",
                subscription: CONTINUOUS,
                hasSkims: true,
                hasDrills: true,
                hasForces: true
            ) {{
            success
            }}
        }}
    """
    data: Dict[str, Any] = {"query": query}
    result = await get_result(data, stakeholder="integratesmanager@gmail.com")
    assert "errors" not in result
    assert "success" in result["data"]["createProject"]
    assert result["data"]["createProject"]["success"]

    group_name2 = await get_name("group")
    query = f"""
        mutation {{
            createProject(
                organization: "{org_name}",
                description: "This is a new project from pytest",
                projectName: "{group_name2}",
                subscription: CONTINUOUS,
                hasSkims: true,
                hasDrills: true,
                hasForces: true
            ) {{
            success
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, stakeholder="integratesmanager@gmail.com")
    assert "errors" not in result
    assert "success" in result["data"]["createProject"]
    assert result["data"]["createProject"]["success"]

    role = "GROUP_MANAGER"
    groupmanager_email = "unittest2@fluidattacks.com"
    query = f"""
        mutation {{
            editStakeholder (
                email: "{groupmanager_email}",
                phoneNumber: "-",
                projectName: "{group_name}",
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
                projectName: "{group_name2}",
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
            addProjectConsult(
                content: "Test consult",
                parent: "0",
                projectName: "{group_name}",
            ) {{
                success
                commentId
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["addProjectConsult"]
    assert result["data"]["addProjectConsult"]["success"]

    query = """
        mutation AddTagsMutation(
            $projectName: String!,
            $tagsData: JSONString!
        ) {
            addTags (
                tags: $tagsData,
                projectName: $projectName) {
                success
            }
        }
    """
    variables = {
        "projectName": group_name,
        "tagsData": json.dumps(["testing"]),
    }
    data = {"query": query, "variables": variables}
    result = await get_result(data)
    assert "errors" not in result
    assert "success" in result["data"]["addTags"]
    assert result["data"]["addTags"]["success"]

    query = f"""
        query {{
            project(projectName: "{group_name}"){{
                name
                hasDrills
                hasForces
                findings {{
                    analyst
                }}
                hasIntegrates
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
    assert result["data"]["project"]["name"] == group_name
    assert result["data"]["project"]["hasDrills"]
    assert result["data"]["project"]["hasForces"]
    assert result["data"]["project"]["hasIntegrates"]
    assert result["data"]["project"]["findings"] == []
    assert result["data"]["project"]["openVulnerabilities"] == 0
    assert result["data"]["project"]["closedVulnerabilities"] == 0
    assert result["data"]["project"]["lastClosingVuln"] == 0
    assert result["data"]["project"]["maxSeverity"] == 0.0
    assert result["data"]["project"]["meanRemediate"] == 0
    assert result["data"]["project"]["meanRemediateLowSeverity"] == 0
    assert result["data"]["project"]["meanRemediateMediumSeverity"] == 0
    assert result["data"]["project"]["openFindings"] == 0
    assert result["data"]["project"]["totalFindings"] == 0
    assert result["data"]["project"]["totalTreatment"] == "{}"
    assert result["data"]["project"]["subscription"] == "continuous"
    assert result["data"]["project"]["deletionDate"] == ""
    assert result["data"]["project"]["userDeletion"] == ""
    assert result["data"]["project"]["tags"] == ["testing"]
    assert (
        result["data"]["project"]["description"]
        == "This is a new project from pytest"
    )
    assert result["data"]["project"]["consulting"] == [
        {"content": "Test consult"}
    ]
    assert result["data"]["project"]["drafts"] == []
    assert result["data"]["project"]["events"] == []
    assert {
        "email": "unittest2@fluidattacks.com",
        "role": "group_manager",
    } in result["data"]["project"]["stakeholders"]
    assert {
        "email": f"forces.{group_name}@fluidattacks.com",
        "role": "service_forces",
    } in result["data"]["project"]["stakeholders"]
    assert result["data"]["project"]["serviceAttributes"] == [
        "has_drills_white",
        "has_forces",
        "has_integrates",
        "is_continuous",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    ]
    assert result["data"]["project"]["bill"] == {"authors": []}

    query = f"""
        query {{
            project(projectName: "{group_name}"){{
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
    assert result["data"]["project"]["findings"] == []

    query = f"""
        query {{
            project(projectName: "{group_name}"){{
                findings(filters: {{affectedSystems: "notexists"}}) {{
                    id
                }}
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data)
    assert "errors" not in result
    assert result["data"]["project"]["findings"] == []

    query = f"""
        mutation {{
            removeTag (
                tag: "testing",
                projectName: "{group_name}",
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
            project(projectName: "{group_name}"){{
                tags
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data)
    assert "errors" not in result
    assert result["data"]["project"]["tags"] == []

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
          group: project(projectName: "{group_name}") {{
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
                hasDrills: false,
                hasForces: false,
                hasIntegrates: false,
                hasSkims: false,
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
            project(projectName: "{group_name}"){{
                hasDrills
                hasForces
                hasIntegrates
                subscription
                __typename
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data)
    assert "errors" in result
    assert result["errors"][0]["message"] == str(UserNotInOrganization())
