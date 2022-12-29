# pylint: disable=too-many-arguments, import-error
from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.test.unit.src.utils import (
    create_dummy_session,
)
from dataloaders import (
    apply_context_attrs,
)
from datetime import (
    datetime,
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
    request = apply_context_attrs(request)  # type: ignore
    _, result = await graphql(SCHEMA, data, context_value=request)

    return result


@pytest.mark.changes_db
async def test_add_group_consult_parent_non_zero() -> None:
    """Check for addGroupConsult mutation."""
    query = """
      mutation {
        addGroupConsult(
          content: "Test comment",
          parentComment: "1545946228675",
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
        "comments",
        "group_name",
        "subscription",
        "has_squad",
        "has_arm",
        "has_machine",
        "reason",
        "expected",
        "tier",
    ],
    [
        # Configuration error, Squad requires ARM
        [
            "",
            "ONESHOTTEST",
            "CONTINUOUS",
            "true",
            "false",
            "true",
            "NONE",
            "Exception - Squad is only available when ASM is too",
            "FREE",
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
            "FREE",
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
            "FREE",
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
            "FREE",
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
            "Value 'ASDF' does not exist in 'UpdateGroupReason' enum.",
            "FREE",
        ],
        # Invalid tier
        [
            "-",
            "UNITTESTING",
            "CONTINUOUS",
            "true",
            "true",
            "true",
            "NONE",
            "Value 'ASDF' does not exist in 'TierType' enum.",
            "ASDF",
        ],
    ],
)
async def test_update_group_bad(  # type: ignore
    comments,
    group_name,
    subscription,
    has_squad,
    has_arm,
    has_machine,
    reason,
    expected,
    tier,
) -> None:
    query = f"""
        mutation {{
            updateGroup(
                comments: "{comments}"
                groupName: "{group_name}",
                hasSquad: {has_squad},
                hasAsm: {has_arm},
                hasMachine: {has_machine},
                reason: {reason},
                subscription: {subscription},
                tier: {tier},
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
            "port": 0,
        },
    ]

    assert result["data"]["serviceWhiteGroup"]["subscription"] == "continuous"
    assert result["data"]["serviceWhiteGroup"]["roots"] == [
        {
            "__typename": "GitRoot",
            "branch": "master",
            "environment": "production",
            "environmentUrls": [
                "https://app.fluidattacks.com",
                "https://test.com",
            ],
            "gitignore": ["bower_components/*", "node_modules/*"],
            "id": "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            "includesHealthCheck": True,
            "url": "https://gitlab.com/fluidattacks/universe",
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

    query_changes = """
      query {
        root(
          groupName: "unittesting"
          rootId: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
        ) {
          ... on GitRoot {
            environmentUrls
            gitEnvironmentUrls {
              url
              id
              createdAt
              secrets {
                value
                key
                description
              }
            }
          }
        }
      }
    """
    result = await _get_result_async({"query": query_changes})
    assert len(result["data"]["root"]["gitEnvironmentUrls"]) > 0
    assert (
        result["data"]["root"]["gitEnvironmentUrls"][0]["id"]
        == "e6118eb4696e04e882362cf2159baf240687256f"
    )
    assert (
        result["data"]["root"]["gitEnvironmentUrls"][0]["url"]
        == result["data"]["root"]["environmentUrls"][0]
    )
    assert (
        datetime.fromisoformat(
            result["data"]["root"]["gitEnvironmentUrls"][0]["createdAt"]
        ).day
        == datetime.now().day
    )


@pytest.mark.changes_db
async def test_update_git_environments_delete() -> None:
    query = """
      mutation {
        updateGitEnvironments(
          groupName: "unittesting"
          id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
          environmentUrls: [
            "https://app.fluidattacks.com/"
            "https://app.fluidattacks.com/a"
            "https://app.fluidattacks.com/b"
          ]
        ) {
          success
        }
      }
    """
    result = await _get_result_async({"query": query})

    assert "errors" not in result
    assert result["data"]["updateGitEnvironments"]["success"]

    query_changes = """
      query {
        root(
          groupName: "unittesting"
          rootId: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
        ) {
          ... on GitRoot {
            environmentUrls
            gitEnvironmentUrls {
              url
              id
              createdAt
            }
          }
        }
      }
    """
    result = await _get_result_async({"query": query_changes})
    assert len(result["data"]["root"]["gitEnvironmentUrls"]) == 3

    query = """
      mutation {
        updateGitEnvironments(
          groupName: "unittesting"
          id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
          environmentUrls: [
            "https://app.fluidattacks.com/"
          ]
          reason: OUT_OF_SCOPE
        ) {
          success
        }
      }
    """
    await _get_result_async({"query": query})

    query_changes = """
      query {
        root(
          groupName: "unittesting"
          rootId: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a"
        ) {
          ... on GitRoot {
            environmentUrls
            gitEnvironmentUrls {
              url
              id
              createdAt
            }
          }
        }
      }
    """
    result = await _get_result_async({"query": query_changes})
    assert len(result["data"]["root"]["gitEnvironmentUrls"]) == 1


@pytest.mark.changes_db
async def test_add_environment_url_secret() -> None:
    query = """
      mutation {
        addGitEnvironmentSecret(
          groupName: "unittesting"
          urlId: "e6118eb4696e04e882362cf2159baf240687256f"
          key: "user"
          value: "jane_doe"
          description: "user acces for prod"
        ) {
          success
        }
      }
    """
    result = await _get_result_async(
        {"query": query}, user="integratesuser@gmail.com"
    )

    assert "errors" not in result
    assert result["data"]["addGitEnvironmentSecret"]["success"]

    query_secrets = """
      query {
        environmentUrl(
          groupName: "unittesting"
          urlId: "e6118eb4696e04e882362cf2159baf240687256f"
        ) {
          url
          id
          secrets {
            key
            value
          }
        }
      }
    """
    result_secrets = await _get_result_async(
        {"query": query_secrets}, user="integrateshacker@fluidattacks.com"
    )
    secrets = result_secrets["data"]["environmentUrl"]["secrets"]
    assert len(secrets) > 0
    assert secrets[0]["key"] == "user"
    assert secrets[0]["value"] == "jane_doe"


@pytest.mark.changes_db
async def test_remove_environment_url_secret() -> None:
    query = """
      mutation {
        removeEnvironmentUrlSecret(
          key: "user"
          groupName: "unittesting"
          urlId: "e6118eb4696e04e882362cf2159baf240687256f"
        ) {
          success
        }
      }
    """
    result = await _get_result_async(
        {"query": query}, user="integratesuser@gmail.com"
    )

    assert "errors" not in result
    assert result["data"]["removeEnvironmentUrlSecret"]["success"]

    query_secrets = """
      query {
        environmentUrl(
          groupName: "unittesting"
          urlId: "e6118eb4696e04e882362cf2159baf240687256f"
        ) {
          url
          id
          secrets {
            key
            value
          }
        }
      }
    """
    result_secrets = await _get_result_async(
        {"query": query_secrets}, user="integrateshacker@fluidattacks.com"
    )
    secrets = result_secrets["data"]["environmentUrl"]["secrets"]
    assert len(secrets) == 0
