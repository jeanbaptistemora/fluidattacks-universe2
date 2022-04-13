# pylint: disable=import-error
from back.test import (
    db,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_files")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
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
                "files": [
                    {
                        "description": "Test",
                        "fileName": "test.zip",
                        "uploadDate": "2019-03-01 15:21",
                        "uploader": "unittest@fluidattacks.com",
                    },
                    {
                        "description": "Test",
                        "fileName": "shell.exe",
                        "uploadDate": "2019-04-24 14:56",
                        "uploader": "unittest@fluidattacks.com",
                    },
                    {
                        "description": "Test",
                        "fileName": "shell2.exe",
                        "uploadDate": "2019-04-24 14:59",
                        "uploader": "unittest@fluidattacks.com",
                    },
                    {
                        "description": "Test",
                        "fileName": "asdasd.py",
                        "uploadDate": "2019-08-06 14:28",
                        "uploader": "unittest@fluidattacks.com",
                    },
                ],
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
