# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.forces.types import (
    ExecutionVulnerabilities,
    ForcesExecution,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("forces_executions")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "executions": [
            {
                "execution": ForcesExecution(
                    group_name="group1",
                    id="123",
                    execution_date="2020-02-05T00:00:00+00:00",
                    exit_code="1",
                    branch="master",
                    commit="6e7b34c1358db2ff4123c3c76e7fe3bf9f2838f6",
                    # FP: local testing
                    origin="http://test.com",  # NOSONAR
                    repo="Repository",
                    grace_period=0,
                    kind="dynamic",
                    severity_threshold=0.0,  # type: ignore
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
