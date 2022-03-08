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
@pytest.mark.resolver_test_group("forces_executions")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "executions": [
            {
                "group_name": "group1",
                "execution_id": "123",
                "date": "2020-02-05T00:00:00Z",
                "exit_code": "1",
                "git_branch": "master",
                "git_commit": "6e7b34c1358db2ff4123c3c76e7fe3bf9f2838f6",
                "git_origin": "http://test.com",
                "git_repo": "Repository",
                "grace_period": 0,
                "kind": "dynamic",
                "severity_threshold": 0.0,
                "strictness": "strict",
                "vulnerabilities": {
                    "num_of_accepted_vulnerabilities": 1,
                    "num_of_open_vulnerabilities": 1,
                    "num_of_closed_vulnerabilities": 1,
                },
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
