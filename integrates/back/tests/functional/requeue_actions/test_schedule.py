from aioextensions import (
    collect,
)
import asyncio
from batch import (
    dal as batch_dal,
)
from more_itertools import (
    side_effect,
)
import pytest
from schedulers import (
    requeue_actions,
)
from unittest import (
    mock,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("requeue_actions")
async def test_requeue_actions(populate: bool) -> None:
    assert populate
    actions_to_delete = [
        "75d0d7e2f4d87093f1084535790ef9d4923e474cd2f431cda3f6b4c34e385a10",
        "636f2162bd48342422e681f29305bbaecb38dd486803fbb1571124e34d145b3e",
        "e5141ac7e052edf0080bc7e0b6032591e79ef2628928d5fb9435bc76e648e8a7",
    ]

    # An action with the same parameters with more resources should be created
    action_to_clone = await batch_dal.get_action(
        action_dynamo_pk="75d0d7e2f4d87093f1084535790ef9d4923e474cd2f431cda3f6b4c34e385a10"
    )
    await collect(
        batch_dal.update_action_to_dynamodb(key=key, running=True)
        for key in actions_to_delete
    )

    read_response = (
        {
            "container": {"vcpus": 4},
            "jobId": "2c95e12c-8b93-4faf-937f-1f2b34530004",
            "status": "FAILED",
        },
        {
            "container": {"vcpus": 8},
            "jobId": "fda5fcbe-8986-4af7-9e54-22a7d8e7981f",
            "status": "FAILED",
        },
        {
            "container": {"vcpus": 4},
            "jobId": "6994b21b-4270-4026-8382-27f35fb6a6e7",
            "status": "SUCCEEDED",
        },
    )
    write_response = ["6fbe3011-eb29-426a-b52d-396382d32c1c"]
    with mock.patch(
        "batch.dal.describe_jobs",
        side_effect=mock.AsyncMock(return_value=read_response),
    ):
        with mock.patch(
            "batch.dal.put_action_to_batch",
            side_effect=mock.AsyncMock(side_effect=write_response),
        ):
            await requeue_actions.main()
            actions = await batch_dal.get_actions()
            actions_ids = [action.key for action in actions]
            assert len(actions) == 1
            assert not any(
                action in actions_ids for action in actions_to_delete
            )
            assert actions[0].action_name == action_to_clone.action_name
            assert (
                actions[0].additional_info == action_to_clone.additional_info
            )
            assert actions[0].entity == action_to_clone.entity
            assert actions[0].queue == action_to_clone.queue
