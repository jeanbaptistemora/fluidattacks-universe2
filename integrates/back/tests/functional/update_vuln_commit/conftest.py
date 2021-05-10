# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from back.tests import (
    db,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vuln_commit")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> None:
    await db.populate(generic_data["db_data"])
    await db.populate(
        {
            "findings": [
                {
                    "finding_id": "475041513",
                    "historic_state": [
                        {
                            "date": "2018-04-07 19:45:11",
                            "analyst": "analyst@gmail.com",
                            "source": "source_path",
                            "state": "APPROVED",
                        },
                    ],
                    "project_name": "group1",
                },
            ],
            "vulnerabilities": [
                {
                    "finding_id": "475041513",
                    "historic_state": [
                        {
                            "date": "2018-04-07 19:45:11",
                            "analyst": "analyst@gmail.com",
                            "source": "integrates",
                            "state": "open",
                        },
                    ],
                    "UUID": "be09edb7-cd5c-47ed-bee4-97c645acdce8",
                    "vuln_type": "ports",
                    "where": "192.168.1.20",
                    "specific": "9999",
                },
            ],
        }
    )
