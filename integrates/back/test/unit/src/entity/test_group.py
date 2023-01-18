from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
from back.test.unit.src.utils import (  # pylint: disable=import-error
    create_dummy_session,
)
from dataloaders import (
    apply_context_attrs,
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
