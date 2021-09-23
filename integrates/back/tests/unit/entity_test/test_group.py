# pylint: disable=too-many-lines, too-many-arguments
from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.tests.unit.utils import (
    create_dummy_session,
)
from dataloaders import (
    apply_context_attrs,
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

pytestmark = pytest.mark.asyncio


async def _get_result_async(
    data: Dict[str, Any], user: str = "integratesmanager@gmail.com"
) -> Dict[str, Any]:
    """Get result."""
    request = await create_dummy_session(username=user)
    request = apply_context_attrs(request)
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result


async def test_group() -> None:
    """Check for group mutation."""
    variables = {"groupName": "unittesting"}
    query = """
      query GetGroupInfo($groupName: String!) {
        group(groupName: $groupName){
          name
          hasSquad
          hasForces
          findings {
              hacker
          }
          hasAsm
          openVulnerabilities
          closedVulnerabilities
          lastClosedVulnerability
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
          consulting {
            content
          }
          drafts {
            age
            openVulnerabilities
          }
          events {
            hacker
            detail
          }
          stakeholders {
            email
            invitationState
            role
            responsibility
            phoneNumber
            firstLogin
            lastLogin
          }
          __typename
        }
      }
    """

    data = {"query": query, "variables": variables}
    result = await _get_result_async(data)

    assert "errors" not in result
    assert result["data"]["group"]["name"] == "unittesting"
    assert result["data"]["group"]["hasSquad"]
    assert result["data"]["group"]["hasForces"]
    assert len(result["data"]["group"]["findings"]) == 6
    assert result["data"]["group"]["openVulnerabilities"] == 31
    assert result["data"]["group"]["closedVulnerabilities"] == 8
    assert "lastClosedVulnerability" in result["data"]["group"]
    assert result["data"]["group"]["maxSeverity"] == 6.3
    assert result["data"]["group"]["meanRemediate"] == 245
    assert result["data"]["group"]["meanRemediateLowSeverity"] == 232
    assert result["data"]["group"]["meanRemediateMediumSeverity"] == 287
    assert result["data"]["group"]["openFindings"] == 5
    assert result["data"]["group"]["totalFindings"] == 6
    assert "totalTreatment" in result["data"]["group"]
    assert result["data"]["group"]["subscription"] == "continuous"
    assert result["data"]["group"]["deletionDate"] == ""
    assert result["data"]["group"]["userDeletion"] == ""
    assert result["data"]["group"]["tags"][0] == "test-projects"
    assert (
        result["data"]["group"]["description"]
        == "Integrates unit test project"
    )
    assert len(result["data"]["group"]["drafts"]) == 1
    assert result["data"]["group"]["drafts"][0]["openVulnerabilities"] == 0
    assert len(result["data"]["group"]["events"]) == 5
    assert (
        result["data"]["group"]["consulting"][0]["content"]
        == "Now we can post comments on projects"
    )
    assert result["data"]["group"]["stakeholders"] == [
        {
            "email": "integratesserviceforces@gmail.com",
            "firstLogin": "2018-02-28 11:54:12",  # NOSONAR
            "invitationState": "CONFIRMED",
            "lastLogin": "2019-10-29 13:40:37",  # NOSONAR
            "phoneNumber": "-",
            "responsibility": "Test",
            "role": "service_forces",
        },
        {
            "email": "integratesmanager@gmail.com",
            "firstLogin": "2018-02-28 11:54:12",
            "invitationState": "CONFIRMED",
            "lastLogin": "2019-12-29 11:50:17",
            "phoneNumber": "-",
            "responsibility": "Test",
            "role": "admin",
        },
        {
            "email": "integratesexecutive@gmail.com",
            "firstLogin": "2018-02-28 11:54:12",
            "invitationState": "CONFIRMED",
            "lastLogin": "2019-10-29 13:40:37",
            "phoneNumber": "-",
            "responsibility": "Test",
            "role": "executive",
        },
        {
            "email": "integratescustomer@gmail.com",
            "firstLogin": "2018-02-28 11:54:12",
            "invitationState": "CONFIRMED",
            "lastLogin": "2019-10-29 13:40:37",
            "phoneNumber": "-",
            "responsibility": "Test",
            "role": "customer",
        },
        {
            "email": "integratesuser@gmail.com",
            "firstLogin": "2018-02-28 11:54:12",
            "invitationState": "CONFIRMED",
            "lastLogin": "2019-10-29 13:40:37",
            "phoneNumber": "-",
            "responsibility": "Test",
            "role": "customeradmin",
        },
        {
            "email": "continuoushacking@gmail.com",
            "firstLogin": "2018-02-28 11:54:12",
            "invitationState": "CONFIRMED",
            "lastLogin": "2020-03-23 10:45:37",
            "phoneNumber": "-",
            "responsibility": "Test",
            "role": "customeradmin",
        },
        {
            "email": "continuoushack2@gmail.com",
            "firstLogin": "2018-02-28 11:54:12",
            "invitationState": "CONFIRMED",
            "lastLogin": "2020-03-23 10:45:37",
            "phoneNumber": "-",
            "responsibility": "Test",
            "role": "customeradmin",
        },
    ]


async def test_group_filtered() -> None:
    """Check for group mutation."""
    query = """
      query {
        group(groupName: "unittesting"){
          findings(filters: {affectedSystems: "test"}) {
            id
          }
        }
      }
    """
    data = {"query": query}
    result = await _get_result_async(data)
    assert "errors" not in result
    assert len(result["data"]["group"]["findings"]) == 2
    assert result["data"]["group"]["findings"][0]["id"] == "463461507"


async def test_group_filter_not_match() -> None:
    """Check for group mutation."""
    query = """
      query {
        group(groupName: "unittesting"){
          findings(filters: {affectedSystems: "notexists"}) {
            id
          }
        }
      }
    """
    data = {"query": query}
    result = await _get_result_async(data)
    assert "errors" not in result
    assert len(result["data"]["group"]["findings"]) == 0


@pytest.mark.changes_db
async def test_add_group() -> None:
    """Check for addGroup mutation."""
    query = """
    mutation {
        addGroup(
            organization: "okada",
            description: "This is a new group from pytest",
            groupName: "%(name)s",
            subscription: CONTINUOUS,
            hasMachine: true,
            hasSquad: true,
        ) {
        success
        }
    }"""
    query = query % {"name": await get_name("group")}
    data = {"query": query}
    result = await _get_result_async(data)
    assert "errors" not in result
    assert "success" in result["data"]["addGroup"]
    assert result["data"]["addGroup"]["success"]


@pytest.mark.changes_db
async def test_add_group_tags() -> None:
    """Check for addGroupTags mutation."""
    query = """
        mutation AddGroupTagsMutation(
          $groupName: String!,
          $tagsData: JSONString!
        ) {
            addGroupTags (
                tags: $tagsData,
                groupName: $groupName) {
                success
            }
        }
        """
    variables = {
        "groupName": "unittesting",
        "tagsData": json.dumps(["testing"]),
    }
    data = {"query": query, "variables": variables}
    result = await _get_result_async(data)
    assert "errors" not in result
    assert "success" in result["data"]["addGroupTags"]
    assert result["data"]["addGroupTags"]["success"]


@pytest.mark.changes_db
async def test_remove_group_tag() -> None:
    """Check for removeGroupTag mutation."""
    query = """
        mutation RemoveGroupTagMutation(
          $tagToRemove: String!,
          $groupName: String!
        ) {
            removeGroupTag (
            tag: $tagToRemove,
            groupName: $groupName,
            ) {
            success
            }
        }
    """
    variables = {"groupName": "oneshottest", "tagToRemove": "another-tag"}
    data = {"query": query, "variables": variables}
    result = await _get_result_async(data)
    assert "errors" not in result
    assert "success" in result["data"]["removeGroupTag"]
    assert result["data"]["removeGroupTag"]["success"]


@pytest.mark.changes_db
async def test_add_group_consult_parent_zero() -> None:
    """Check for addGroupConsult mutation."""
    query = """
      mutation {
        addGroupConsult(
          content: "Test comment",
          parent: "0",
          groupName: "unittesting",
        ) {
          success
          commentId
        }
      }
      """
    data = {"query": query}
    result = await _get_result_async(data)
    assert "errors" not in result
    assert "success" in result["data"]["addGroupConsult"]
    assert result["data"]["addGroupConsult"]["success"]


@pytest.mark.changes_db
async def test_add_group_consult_parent_non_zero() -> None:
    """Check for addGroupConsult mutation."""
    query = """
      mutation {
        addGroupConsult(
          content: "Test comment",
          parent: "1545946228675",
          groupName: "unittesting",
        ) {
          success
          commentId
        }
      }
      """
    data = {"query": query}
    result = await _get_result_async(data)
    assert "errors" not in result
    assert "success" in result["data"]["addGroupConsult"]
    assert result["data"]["addGroupConsult"]["success"]


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        "group_name",
        "subscription",
        "has_squad",
        "has_asm",
        "has_machine",
        "expected",
    ],
    [
        ["UNITTESTING", "CONTINUOUS", "true", "true", "true", True],
        ["ONESHOTTEST", "ONESHOT", "false", "true", "false", True],
    ],
)
async def test_update_group_good(  # type: ignore
    group_name,
    subscription,
    has_squad,
    has_asm,
    has_machine,
    expected,
) -> None:
    query = f"""
        mutation {{
            updateGroup(
                comments: "",
                groupName: "{group_name}",
                subscription: {subscription},
                hasSquad: {has_squad},
                hasAsm: {has_asm},
                hasMachine: {has_machine},
                reason: NONE,
            ) {{
                success
            }}
        }}
      """
    result = await _get_result_async({"query": query})

    assert "errors" not in result
    assert "success" in result["data"]["updateGroup"]
    assert result["data"]["updateGroup"]["success"] == expected


@pytest.mark.changes_db
@pytest.mark.parametrize(
    [
        "comments",
        "group_name",
        "subscription",
        "has_squad",
        "has_asm",
        "has_machine",
        "reason",
        "expected",
    ],
    [
        # Configuration error, Squad requires ASM
        [
            "",
            "ONESHOTTEST",
            "CONTINUOUS",
            "true",
            "false",
            "true",
            "NONE",
            "Exception - Squad is only available when ASM is too",
        ],
        # Configuration error, Squad requires Machine
        [
            "",
            "ONESHOTTEST",
            "CONTINUOUS",
            "true",
            "true",
            "false",
            "NONE",
            "Exception - Squad is only available when Machine is too",
        ],
        # Input validation error, weird chars
        [
            "\xFF",
            "UNITTESTING",
            "CONTINUOUS",
            "true",
            "true",
            "true",
            "NONE",
            "Exception - Invalid characters",
        ],
        # Input validation error, too long string
        [
            "-" * 251,
            "UNITTESTING",
            "CONTINUOUS",
            "true",
            "true",
            "true",
            "NONE",
            "Exception - Invalid field length in form",
        ],
        # Invalid reason
        [
            "-",
            "UNITTESTING",
            "CONTINUOUS",
            "true",
            "true",
            "true",
            "ASDF",
            "Expected type UpdateGroupReason, found ASDF.",
        ],
    ],
)
async def test_update_group_bad(  # type: ignore
    comments,
    group_name,
    subscription,
    has_squad,
    has_asm,
    has_machine,
    reason,
    expected,
) -> None:
    query = f"""
        mutation {{
            updateGroup(
                comments: "{comments}"
                groupName: "{group_name}",
                hasSquad: {has_squad},
                hasAsm: {has_asm},
                hasMachine: {has_machine},
                reason: {reason},
                subscription: {subscription},
            ) {{
                success
            }}
        }}
      """
    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert result["errors"][0]["message"] == expected


async def test_get_roots() -> None:
    query = """
        query {
          serviceBlackGroup: group(groupName: "oneshottest") {
            roots {
              __typename
              ...on IPRoot {
                address
                id
                port
              }
              ...on URLRoot {
                host
                id
                path
                port
                protocol
              }
            }
            subscription
          }
          serviceWhiteGroup: group(groupName: "unittesting") {
            roots {
              __typename
              ...on GitRoot {
                branch
                environment
                environmentUrls
                gitignore
                id
                includesHealthCheck
                url
              }
            }
            subscription
          }
        }
    """
    result = await _get_result_async({"query": query})

    assert "errors" not in result
    assert result["data"]["serviceBlackGroup"]["subscription"] == "oneshot"
    assert result["data"]["serviceBlackGroup"]["roots"] == [
        {
            "__typename": "URLRoot",
            "host": "app.fluidattacks.com",
            "id": "8493c82f-2860-4902-86fa-75b0fef76034",
            "path": "/",
            "port": 443,
            "protocol": "HTTPS",
        },
        {
            "__typename": "IPRoot",
            "address": "127.0.0.1",
            "id": "d312f0b9-da49-4d2b-a881-bed438875e99",
            "port": 8080,
        },
    ]

    assert result["data"]["serviceWhiteGroup"]["subscription"] == "continuous"
    assert result["data"]["serviceWhiteGroup"]["roots"] == [
        {
            "__typename": "GitRoot",
            "branch": "master",
            "environment": "production",
            "environmentUrls": ["https://app.fluidattacks.com"],
            "gitignore": ["bower_components/*", "node_modules/*"],
            "id": "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            "includesHealthCheck": True,
            "url": "https://gitlab.com/fluidattacks/product",
        },
        {
            "__typename": "GitRoot",
            "branch": "develop",
            "environment": "QA",
            "environmentUrls": [],
            "gitignore": [],
            "id": "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            "includesHealthCheck": False,
            "url": "https://gitlab.com/fluidattacks/integrates",
        },
    ]


async def test_get_toe_lines() -> None:
    query = """
      query {
        group(groupName: "unittesting"){
          name
          roots{
            ... on GitRoot {
              id
              toeLines {
                filename
                modifiedDate
                modifiedCommit
                loc
                testedDate
                testedLines
                comments
              }
            }
          }
        }
      }
    """
    result = await _get_result_async(
        {"query": query}, user="unittest2@fluidattacks.com"
    )
    assert "errors" not in result
    assert result["data"]["group"]["roots"] == [
        {
            "id": "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            "toeLines": [
                {
                    "filename": "product/test/test#.config",
                    "modifiedDate": "2019-08-01T00:00:00-05:00",
                    "modifiedCommit": "983466z",
                    "loc": 8,
                    "testedDate": "2021-02-28T00:00:00-05:00",
                    "testedLines": 4,
                    "comments": "comment test",
                }
            ],
        },
        {
            "id": "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            "toeLines": [
                {
                    "filename": "integrates_1/test2/test.sh",
                    "modifiedDate": "2020-11-19T00:00:00-05:00",
                    "modifiedCommit": "273412t",
                    "loc": 172,
                    "testedDate": "2021-01-20T00:00:00-05:00",
                    "testedLines": 120,
                    "comments": "comment test",
                }
            ],
        },
    ]


async def test_add_git_root_black() -> None:
    query = """
      mutation {
        addGitRoot(
          branch: "master"
          environment: "Test"
          gitignore: []
          groupName: "oneshottest"
          includesHealthCheck: false
          url: "https://gitlab.com/fluidattacks/integrates"
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"  # NOSONAR


@pytest.mark.changes_db
async def test_add_git_root_white() -> None:
    query = """
      mutation {
        addGitRoot(
          branch: "master"
          environment: "production"
          gitignore: []
          groupName: "unittesting"
          includesHealthCheck: true
          url: "https://gitlab.com/fluidattacks/integrates"
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" not in result
    assert result["data"]["addGitRoot"]["success"]


async def test_add_git_root_invalid_branch() -> None:
    query = """
      mutation {
        addGitRoot(
          branch: "( ͡° ͜ʖ ͡°)"
          environment: "Test"
          gitignore: []
          groupName: "unittesting"
          includesHealthCheck: false
          url: "https://gitlab.com/fluidattacks/integrates"
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert "value is not valid" in result["errors"][0]["message"]  # NOSONAR


async def test_add_git_root_invalid_url() -> None:
    query = """
      mutation {
        addGitRoot(
          branch: "master"
          environment: "Test"
          gitignore: []
          groupName: "unittesting"
          includesHealthCheck: false
          url: "randomstring"
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert "value is not valid" in result["errors"][0]["message"]


@pytest.mark.changes_db
async def test_add_git_root_uniqueness() -> None:
    query = """
      mutation {
        addGitRoot(
          branch: "unique"
          environment: "unique"
          gitignore: []
          groupName: "unittesting"
          includesHealthCheck: false
          url: "https://gitlab.com/fluidattacks/unique.git"
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" not in result
    assert result["data"]["addGitRoot"]["success"]

    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert "same Nickname already exists" in result["errors"][0]["message"]


@pytest.mark.changes_db
async def test_add_ip_root_black() -> None:
    query = """
      mutation {
        addIpRoot(
          address: "8.8.8.8"
          groupName: "oneshottest"
          nickname: "test_ip"
          port: 53
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" not in result
    assert result["data"]["addIpRoot"]["success"]


async def test_add_ip_root_white() -> None:
    query = """
      mutation {
        addIpRoot(
          address: "8.8.8.8"
          groupName: "unittesting"
          nickname: "test_ip"
          port: 53
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


async def test_add_ip_root_invalid_ip() -> None:
    query = """
      mutation {
        addIpRoot(
          address: "randomstr"
          groupName: "oneshottest"
          nickname: "test_ip"
          port: 53
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert "value is not valid" in result["errors"][0]["message"]


async def test_add_ip_root_invalid_port() -> None:
    query = """
      mutation {
        addIpRoot(
          address: "8.8.8.8"
          groupName: "oneshottest"
          nickname: "test_ip"
          port: -2600
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert "value is not valid" in result["errors"][0]["message"]


@pytest.mark.changes_db
async def test_add_ip_root_uniqueness() -> None:
    query = """
      mutation {
        addIpRoot(
          address: "1.1.1.1"
          groupName: "oneshottest"
          nickname: "test_ip_1"
          port: 53
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" not in result
    assert result["data"]["addIpRoot"]["success"]

    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert "already exists" in result["errors"][0]["message"]


@pytest.mark.changes_db
async def test_add_url_root_black() -> None:
    query = """
      mutation {
        addUrlRoot(
          groupName: "oneshottest",
          nickname: "test_url"
          url: "https://fluidattacks.com/"
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" not in result
    assert result["data"]["addUrlRoot"]["success"]


async def test_add_url_root_white() -> None:
    query = """
      mutation {
        addUrlRoot(
          groupName: "unittesting",
          nickname: "test_url"
          url: "https://fluidattacks.com/"
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


async def test_add_url_root_invalid_url() -> None:
    query = """
      mutation {
        addUrlRoot(
          groupName: "oneshottest"
          nickname: "test_url"
          url: "randomstring"
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert "value is not valid" in result["errors"][0]["message"]


async def test_add_url_root_invalid_protocol() -> None:
    query = """
      mutation {
        addUrlRoot(
          groupName: "oneshottest"
          nickname: "test_url"
          url: "ssh://test.com:22"
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert "value is not valid" in result["errors"][0]["message"]


@pytest.mark.changes_db
async def test_add_url_root_uniqueness() -> None:
    query = """
      mutation {
        addUrlRoot(
          groupName: "oneshottest"
          nickname: "test_url_1"
          url: "https://unique.com/"
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" not in result
    assert result["data"]["addUrlRoot"]["success"]

    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert "already exists" in result["errors"][0]["message"]


@pytest.mark.changes_db
async def test_update_git_root() -> None:
    query = """
      mutation {
        updateGitRoot(
          branch: "develop"
          environment: "staging"
          gitignore: []
          groupName: "unittesting"
          id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
          includesHealthCheck: false
          nickname: "randomNick"
          url: "https://gitlab.com/fluidattacks/integrates"
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" not in result
    assert result["data"]["updateGitRoot"]["success"]


async def test_update_git_root_nonexistent() -> None:
    query = """
      mutation {
        updateGitRoot(
          branch: ""
          environment: "Test"
          gitignore: []
          groupName: "unittesting"
          id: "some-thing"
          includesHealthCheck: false
          nickname: "unique2"
          url: ""
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert "root not found" in result["errors"][0]["message"]  # NOSONAR


@pytest.mark.changes_db
async def test_update_git_environments() -> None:
    query = """
      mutation {
        updateGitEnvironments(
          groupName: "unittesting"
          id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
          environmentUrls: ["https://app.fluidattacks.com/"]
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" not in result
    assert result["data"]["updateGitEnvironments"]["success"]


@pytest.mark.changes_db
async def test_update_root_cloning_status() -> None:
    query = """
    mutation {
      updateRootCloningStatus(
        groupName: "unittesting"
        id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
        status: OK
        message: "root update test"
      ) {
        success
      }
    }
  """
    result = await _get_result_async({"query": query})

    assert "errors" not in result
    assert result["data"]["updateRootCloningStatus"]["success"]


@pytest.mark.changes_db
async def test_update_root_cloning_status_nonexistent() -> None:
    query = """
    mutation {
      updateRootCloningStatus(
        groupName: "unittesting"
        id: "4039d098-ffc5-4984-8ed3-eb17bca98e199"
        status: OK
        message: "root update test"
      ) {
        success
      }
    }
  """
    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert "root not found" in result["errors"][0]["message"]


@pytest.mark.changes_db
async def test_deactivate_root() -> None:
    query = """
      mutation {
        deactivateRoot(
          groupName: "unittesting"
          id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
          reason: OTHER
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" not in result
    assert result["data"]["deactivateRoot"]["success"]


async def test_deactivate_root_nonexistent() -> None:
    query = """
      mutation {
        deactivateRoot(
          groupName: "unittesting"
          id: "some-thing"
          reason: OTHER
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" in result
    assert "root not found" in result["errors"][0]["message"]


@pytest.mark.changes_db
async def test_unsubscribe_from_group() -> None:
    query = """
      mutation {
        unsubscribeFromGroup(groupName: "metropolis"){
          success
        }
      }
    """
    result = await _get_result_async(
        {"query": query}, user="integratesuser@gmail.com"
    )

    assert "errors" not in result
    assert result["data"]["unsubscribeFromGroup"]["success"]
