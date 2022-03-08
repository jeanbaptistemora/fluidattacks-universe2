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
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
