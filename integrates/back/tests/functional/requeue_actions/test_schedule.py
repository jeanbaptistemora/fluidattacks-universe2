from aioextensions import (
    collect,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Action,
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
    running_actions = actions_to_delete + [
        "d594e2851fe5d537742959291fbff448758dfab9b8bee35047f000c6e1fc0402"
    ]

    # An action with the same parameters with more resources should be created
    action_to_clone = await batch_dal.get_action(
        action_dynamo_pk="75d0d7e2f4d87093f1084535790ef9d4923e474cd2f431cda3f6b4c34e385a10"
    )

    await collect(
        batch_dal.update_action_to_dynamodb(key=key, running=True)
        for key in running_actions
    )

    # An active action that will not have any changes
    unchanged_action = await batch_dal.get_action(
        action_dynamo_pk="d594e2851fe5d537742959291fbff448758dfab9b8bee35047f000c6e1fc0402"
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
        {
            "container": {"vcpus": 2},
            "jobId": "342cea18-72b5-49c0-badb-f7e38dd0e273",
            "status": "RUNNING",
        },
    )
    write_response = [
        "6fbe3011-eb29-426a-b52d-396382d32c1c",
        "2507485d-4a2e-4c14-a68b-fbe0c34d5f01",
    ]
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
            assert len(actions) == 3
            assert not any(
                action in actions_ids for action in actions_to_delete
            )

            machine_action = next(
                action
                for action in actions
                if action.action_name == Action.EXECUTE_MACHINE.value
            )
            assert machine_action.action_name == action_to_clone.action_name
            assert (
                machine_action.additional_info
                == action_to_clone.additional_info
            )
            assert machine_action.entity == action_to_clone.entity
            assert machine_action.queue == action_to_clone.queue

            clone_action = next(
                action
                for action in actions
                if action.action_name == Action.CLONE_ROOTS.value
            )
            assert (
                clone_action.batch_job_id
                == "2507485d-4a2e-4c14-a68b-fbe0c34d5f01"
            )
            assert not clone_action.running

            assert unchanged_action in actions
