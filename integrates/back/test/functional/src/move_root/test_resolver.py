# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Action,
)
from custom_exceptions import (
    InvalidParameter,
)
from dataloaders import (
    get_new_context,
)
import pytest
from typing import (
    Any,
)


async def resolve(
    *,
    group_name: str,
    root_id: str,
    user: str,
) -> dict[str, Any]:
    query: str = f"""
        query {{
            root(groupName: "{group_name}", rootId: "{root_id}") {{
                ... on GitRoot {{
                    state
                }}
                ... on IPRoot {{
                    state
                }}
                ... on URLRoot {{
                    state
                }}
            }}
        }}
    """
    data = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def mutate(
    *,
    root_id: str,
    source_group_name: str,
    target_group_name: str,
    user: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            moveRoot(
                groupName: "{source_group_name}",
                id: "{root_id}",
                targetGroupName: "{target_group_name}"
            ) {{
                success
            }}
        }}
    """
    data = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("move_root")
async def test_should_mutate_successfully(populate: bool) -> None:
    assert populate
    result = await resolve(
        group_name="kibi",
        root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
        user="test@fluidattacks.com",
    )
    batch_actions = await batch_dal.get_actions()
    assert result["data"]["root"]["state"] == "ACTIVE"
    assert len(batch_actions) == 0

    result = await mutate(
        root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
        source_group_name="kibi",
        target_group_name="kuri",
        user="test@fluidattacks.com",
    )
    assert "errors" not in result
    assert "success" in result["data"]["moveRoot"]
    assert result["data"]["moveRoot"]["success"]

    result = await resolve(
        group_name="kibi",
        root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
        user="test@fluidattacks.com",
    )
    assert result["data"]["root"]["state"] == "INACTIVE"
    batch_actions = await batch_dal.get_actions()
    assert len(batch_actions) == 3

    action_names = tuple(action.action_name for action in batch_actions)
    assert Action.MOVE_ROOT.value in action_names
    assert Action.REFRESH_TOE_LINES.value in action_names
    assert Action.REFRESH_TOE_INPUTS.value in action_names


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("move_root")
@pytest.mark.parametrize(
    ("root_id", "source_group_name", "target_group_name"),
    (
        # Inactive root
        (
            "8a62109b-316a-4a88-a1f1-767b80383864",
            "kibi",
            "kuri",
        ),
        # Same group
        (
            "88637616-41d4-4242-854a-db8ff7fe1ab6",
            "kibi",
            "kibi",
        ),
        # Target group outside the organization
        (
            "88637616-41d4-4242-854a-db8ff7fe1ab6",
            "kibi",
            "kurau",
        ),
        # Groups with different services
        (
            "88637616-41d4-4242-854a-db8ff7fe1ab6",
            "kibi",
            "udon",
        ),
    ),
)
async def test_should_trigger_validations(
    populate: bool,
    root_id: str,
    source_group_name: str,
    target_group_name: str,
) -> None:
    assert populate
    result = await mutate(
        root_id=root_id,
        source_group_name=source_group_name,
        target_group_name=target_group_name,
        user="test@fluidattacks.com",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == InvalidParameter().args[0]
