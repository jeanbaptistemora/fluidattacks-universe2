from back.tests import (
    db,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("requeue_actions")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data = {
        "actions": (
            {
                "action_name": "execute-machine",
                "additional_info": "{'roots': ['nickname1', 'nickname2'], 'checks': ['F001', 'F002']}",
                "batch_job_id": "2c95e12c-8b93-4faf-937f-1f2b34530004",
                "entity": "group1",
                "key": "75d0d7e2f4d87093f1084535790ef9d4923e474cd2f431cda3f6b4c34e385a10",
                "queue": "skims_all_soon",
                "subject": "unittesting@fluidattacks.com",
                "time": "1646769443",
            },
            {
                "action_name": "execute-machine",
                "additional_info": "{'roots': ['nickname1'], 'checks': ['F001', 'F002']}",
                "batch_job_id": "fda5fcbe-8986-4af7-9e54-22a7d8e7981f",
                "entity": "group2",
                "key": "636f2162bd48342422e681f29305bbaecb38dd486803fbb1571124e34d145b3e",
                "queue": "skims_all_later",
                "subject": "unittesting@fluidattacks.com",
                "time": "1646769443",
            },
            {
                "action_name": "execute-machine",
                "additional_info": "{'roots': ['nickname1'], 'checks': ['F001', 'F002', 'F003']}",
                "batch_job_id": "6994b21b-4270-4026-8382-27f35fb6a6e7",
                "entity": "group3",
                "key": "e5141ac7e052edf0080bc7e0b6032591e79ef2628928d5fb9435bc76e648e8a7",
                "queue": "skims_all_soon",
                "subject": "unittesting@fluidattacks.com",
                "time": "1646773865",
            },
            {
                "action_name": "clone_roots",
                "additional_info": "nickname1,nickname2",
                "batch_job_id": "c8a18de6-2403-461c-9d77-991041a9632a",
                "entity": "group4",
                "key": "5836c88c53849c19f01868e4c42f491444a14f019362ab9093714d942e115bc9",
                "queue": "spot_soon",
                "subject": "unittesting@fluidattacks.com",
                "time": "1646773865",
            },
            {
                "action_name": "refresh_toe_lines",
                "additional_info": "nickname3",
                "batch_job_id": "342cea18-72b5-49c0-badb-f7e38dd0e273",
                "entity": "group5",
                "key": "d594e2851fe5d537742959291fbff448758dfab9b8bee35047f000c6e1fc0402",
                "queue": "spot_soon",
                "subject": "unittesting@fluidattacks.com",
                "time": "1646773865",
            },
            {
                "action_name": "refresh_toe_inputs",
                "additional_info": "nickname4",
                "batch_job_id": "42d5b400-89f3-498c-b7ce-cc29d2e7f254",
                "entity": "group6",
                "key": "0d9c88b99f14107958d5a4e68af1c8bf8c30222ad639c0187ff734383bd22641",
                "queue": "spot_later",
                "subject": "unittesting@fluidattacks.com",
                "time": "1646773865",
            },
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
