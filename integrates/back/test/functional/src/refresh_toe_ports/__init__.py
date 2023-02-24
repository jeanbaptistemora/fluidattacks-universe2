# pylint: disable=import-error
from _pytest.monkeypatch import (
    MonkeyPatch,
)
from back.test.functional.src.utils import (
    get_batch_job,
    get_graphql_result,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Action,
    Product,
)
from batch_dispatch import (
    dispatch,
)
from dataloaders import (
    get_new_context,
)
import sys
from typing import (
    Any,
)


async def refresh_toe_ports(
    *,
    user: str,
    group_name: str,
    monkeypatch: MonkeyPatch,
) -> None:
    await batch_dal.put_action(
        action=Action.REFRESH_TOE_PORTS,
        entity=group_name,
        subject=user,
        additional_info="*",
        queue=batch_dal.IntegratesBatchQueue.SMALL,
        product_name=Product.INTEGRATES,
    )
    batch_action = await get_batch_job(
        action_name="refresh_toe_ports", entity=group_name
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "test",
            batch_action.key,
        ],
    )
    await dispatch.dispatch()


async def query_get(
    *,
    user: str,
    group_name: str,
) -> dict[str, Any]:
    query: str = f"""{{
        group(groupName: "{group_name}"){{
            toePorts {{
                edges {{
                    node {{
                        address
                        attackedAt
                        attackedBy
                        bePresent
                        bePresentUntil
                        firstAttackAt
                        seenAt
                        seenFirstTimeBy
                        hasVulnerabilities
                        port
                        root {{
                            __typename
                            id
                            nickname
                        }}
                    }}
                    cursor
                }}
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
            }}
        }}
      }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
