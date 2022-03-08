# pylint: disable=import-error
from back.tests import (
    db,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("event")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "events": [
            {
                "group_name": "group1",
                "event_id": "418900971",
                "accessibility": "Repositorio",
                "affected_components": "affected_components_test",
                "action_after_blocking": "EXECUTE_OTHER_GROUP_SAME_CLIENT",
                "action_before_blocking": "TEST_OTHER_PART_TOE",
                "analyst": "unittest@fluidattacks.com",
                "client": "Fluid",
                "client_project": "group1",
                "closer": "unittest",
                "closing_date": "2018-06-27 14:40:05",
                "context": "FLUID",
                "detail": "ASM unit test",
                "historic_state": [
                    {
                        "analyst": "unittest@fluidattacks.com",
                        "date": "2018-06-27 07:00:00",
                        "state": "OPEN",
                    },
                    {
                        "analyst": "unittest@fluidattacks.com",
                        "date": "2018-06-27 14:40:05",
                        "state": "CREATED",
                    },
                ],
                "event_type": "OTHER",
                "hours_before_blocking": "1",
                "subscription": "ONESHOT",
                "evidence": "1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6",
                "evidence_date": "2019-03-11 10:57:45",
                "evidence_file": "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad",
                "evidence_file_date": "2019-03-11 10:57:45",
            },
        ],
        "comments": [
            {
                "finding_id": "418900971",
                "comment_id": "43455343453",
                "comment_type": "event",
                "content": "This is a test comment",
                "created": "2019-05-28 15:09:37",
                "email": "admin@gmail.com",
                "fullname": "test one",
                "modified": "2019-05-28 15:09:37",
                "parent": 0,
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
