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
@pytest.mark.resolver_test_group("remove_group_tag")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "groups": [
            {
                "project_name": "group1",
                "description": "-",
                "language": "en",
                "historic_configuration": [
                    {
                        "date": "2020-05-20 17:00:00",
                        "has_drills": False,
                        "has_forces": False,
                        "requester": "unknown",
                        "service": "WHITE",
                        "type": "continuous",
                    }
                ],
                "project_status": "ACTIVE",
                "tag": [
                    "test1",
                    "test2",
                    "test3",
                    "test4",
                    "test5",
                ],
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
