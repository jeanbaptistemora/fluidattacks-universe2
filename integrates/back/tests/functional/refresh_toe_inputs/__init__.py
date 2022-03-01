from _pytest.monkeypatch import (
    MonkeyPatch,
)
from back.tests.functional.utils import (
    get_batch_job,
    get_graphql_result,
)
from batch import (
    dal as batch_dal,
    dispatch,
)
from batch.enums import (
    Action,
    Product,
)
from dataloaders import (
    get_new_context,
)
import sys
from typing import (
    Any,
    Dict,
)


async def refresh_toe_inputs(
    *,
    user: str,
    group_name: str,
    monkeypatch: MonkeyPatch,
) -> None:
    await batch_dal.put_action(
        action=Action.REFRESH_TOE_INPUTS,
        entity=group_name,
        subject=user,
        additional_info="*",
        product_name=Product.INTEGRATES,
    )
    batch_action = await get_batch_job(
        action_name="refresh_toe_inputs", entity=group_name
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "test",
            batch_action.key,
        ],
    )
    await dispatch.main()


async def query_get(
    *,
    user: str,
    group_name: str,
) -> Dict[str, Any]:
    query: str = f"""{{
        group(groupName: "{group_name}"){{
            toeInputs {{
                edges {{
                    node {{
                       attackedAt
                        attackedBy
                        bePresent
                        bePresentUntil
                        component
                        entryPoint
                        firstAttackAt
                        seenAt
                        seenFirstTimeBy
                        root {{
                            ... on GitRoot {{
                            __typename
                            id
                            nickname
                            }}
                            ... on IPRoot {{
                            __typename
                            id
                            nickname
                            }}
                            ... on URLRoot {{
                            __typename
                            id
                            nickname
                            }}
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
    data: Dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
