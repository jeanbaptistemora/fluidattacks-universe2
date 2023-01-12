# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.forces.types import (
    ExecutionVulnerabilities,
    ForcesExecution,
)
from decimal import (
    Decimal,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("forces_executions")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "executions": [
            {
                "execution": ForcesExecution(
                    group_name="group1",
                    id="123",
                    execution_date=datetime.fromisoformat(
                        "2020-02-05T00:00:00+00:00"
                    ),
                    exit_code="1",
                    branch="master",
                    commit="6e7b34c1358db2ff4123c3c76e7fe3bf9f2838f6",
                    # FP: local testing
                    origin="http://test.com",  # NOSONAR
                    repo="Repository",
                    grace_period=0,
                    kind="dynamic",
                    severity_threshold=Decimal("0.0"),
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
