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

    # An active action that will not have any changes
    unchanged_actions = await collect(
        batch_dal.get_action(action_dynamo_pk=pk)
        for pk in [
            "d594e2851fe5d537742959291fbff448758dfab9b8bee35047f000c6e1fc0402",
            "0d9c88b99f14107958d5a4e68af1c8bf8c30222ad639c0187ff734383bd22641",
        ]
    )

    read_response = (
        {
            "container": {
                "resourceRequirements": [
                    {"value": "2", "type": "VCPU"},
                    {"value": "3200", "type": "MEMORY"},
                ],
            },
            "jobId": "2c95e12c-8b93-4faf-937f-1f2b34530004",
            "status": "FAILED",
        },
        {
            "container": {
                "resourceRequirements": [
                    {"value": "8", "type": "VCPU"},
                    {"value": "1800", "type": "MEMORY"},
                ],
            },
            "jobId": "fda5fcbe-8986-4af7-9e54-22a7d8e7981f",
            "status": "FAILED",
        },
        {
            "container": {
                "resourceRequirements": [
                    {"value": "2", "type": "VCPU"},
                    {"value": "1800", "type": "MEMORY"},
                ],
            },
            "jobId": "6994b21b-4270-4026-8382-27f35fb6a6e7",
            "status": "SUCCEEDED",
        },
        {
            "container": {
                "resourceRequirements": [
                    {"value": "2", "type": "VCPU"},
                    {"value": "1800", "type": "MEMORY"},
                ],
            },
            "jobId": "342cea18-72b5-49c0-badb-f7e38dd0e273",
            "status": "RUNNING",
        },
        {
            "container": {
                "resourceRequirements": [
                    {"value": "1", "type": "VCPU"},
                    {"value": "1800", "type": "MEMORY"},
                ],
            },
            "jobId": "42d5b400-89f3-498c-b7ce-cc29d2e7f254",
            "status": "RUNNABLE",
        },
    )
    # create jobs in dynamo
    await collect(
        batch_dal.update_action_to_dynamodb(
            key=key, running=True, batch_job_id=read_response[index]["jobId"]
        )
        for index, key in enumerate(running_actions)
    )
    write_response = [
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

            clone_action = next(
                action
                for action in actions
                if action.action_name == Action.CLONE_ROOTS.value
            )
            assert (
                clone_action.batch_job_id
                == "2507485d-4a2e-4c14-a68b-fbe0c34d5f01"
            )
            assert clone_action.running is False
            assert any(
                unchanged_action in actions
                for unchanged_action in unchanged_actions
            )
