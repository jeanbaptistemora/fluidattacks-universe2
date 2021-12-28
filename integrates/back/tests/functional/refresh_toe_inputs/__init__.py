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
        action_name="refresh_toe_inputs",
        entity=group_name,
        subject=user,
        additional_info="*",
    )
    batch_action = await get_batch_job(
        action_name="refresh_toe_inputs", entity=group_name
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "test",
            batch_action.action_name,
            batch_action.subject,
            batch_action.entity,
            batch_action.time,
            batch_action.additional_info,
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
                        unreliableRootNickname
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
