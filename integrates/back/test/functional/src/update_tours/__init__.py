# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
from typing import (
    Any,
)


async def get_result(*, user: str, tours: dict[str, bool]) -> dict[str, Any]:
    query: str = f"""
    mutation {{
    updateTours(tours:
    {{
        newGroup: {tours["newGroup"]},
        newRiskExposure: {tours["newRiskExposure"]},
        newRoot: {tours["newRoot"]},
        welcome: {tours["welcome"]} }})
    {{
      success
        }}
    }}"""
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
