# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.forces.types import (
    ExecutionVulnerabilities,
    ForcesExecution,
)
from newutils.datetime import (
    get_as_str,
    get_from_str,
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
    datetime = get_from_str(
        "2020-02-05T00:00:00Z",
        date_format="%Y-%m-%dT%H:%M:%SZ",
        zone="UTC",
    )
    data: Dict[str, Any] = {
        "executions": [
            {
                "execution": ForcesExecution(
                    group_name="group1",
                    id="123",
                    execution_date=get_as_str(
                        date=datetime,
                        date_format="%Y-%m-%dT%H:%M:%S.%f%z",
                        zone="UTC",
                    ),
                    exit_code="1",
                    branch="master",
                    commit="6e7b34c1358db2ff4123c3c76e7fe3bf9f2838f6",
                    origin="http://test.com",
                    repo="Repository",
                    grace_period=0,
                    kind="dynamic",
                    severity_threshold=0.0,
                    strictness="strict",
                    vulnerabilities=ExecutionVulnerabilities(
                        num_of_accepted_vulnerabilities=1,
                        num_of_open_vulnerabilities=1,
                        num_of_closed_vulnerabilities=1,
                    ),
                ),
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
