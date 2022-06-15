# pylint: disable=import-error
from back.test import (
    db,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_event_evidence")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "events": [
            {
                "project_name": "group1",
                "event_id": "418900971",
                "accessibility": "Repositorio",
                "affected_components": "Otro(s)",
                "analyst": generic_data["global_vars"]["hacker_email"],
                "client": "Fluid",
                "client_project": "group1",
                "closer": "unittest",
                "closing_date": "2018-06-27 14:40:05",
                "detail": "ASM unit test1",
                "historic_state": [
                    {
                        "analyst": generic_data["global_vars"]["hacker_email"],
                        "date": "2018-06-27 07:00:00",
                        "state": "OPEN",
                    },
                    {
                        "analyst": generic_data["global_vars"]["hacker_email"],
                        "date": "2018-06-27 13:40:05",
                        "state": "CREATED",
                    },
                ],
                "event_type": "OTHER",
                "subscription": "ONESHOT",
                "evidence": "1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6",
                "evidence_date": "2019-03-11 10:57:45",
                "evidence_file": "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad",
                "evidence_file_date": "2019-03-11 10:57:45",
            },
            {
                "project_name": "group1",
                "event_id": "418900972",
                "accessibility": "Repositorio",
                "affected_components": "Otro(s)",
                "analyst": generic_data["global_vars"]["hacker_email"],
                "client": "Fluid",
                "client_project": "group1",
                "closer": "unittest",
                "closing_date": "2018-06-27 12:40:05",
                "detail": "ASM unit test2",
                "historic_state": [
                    {
                        "analyst": generic_data["global_vars"]["hacker_email"],
                        "date": "2018-06-27 07:00:00",
                        "state": "OPEN",
                    },
                    {
                        "analyst": generic_data["global_vars"]["hacker_email"],
                        "date": "2018-06-27 11:40:05",
                        "state": "CREATED",
                    },
                ],
                "event_type": "OTHER",
                "subscription": "ONESHOT",
                "evidence": "1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6",
                "evidence_date": "2019-03-11 11:57:45",
                "evidence_file": "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad",
                "evidence_file_date": "2019-03-11 11:57:45",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
