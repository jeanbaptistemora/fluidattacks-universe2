# pylint: disable=import-error
from back.test import (
    db,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("solve_event")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "evnts": [
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
                        "date": "2018-06-27 12:40:05",
                        "state": "CREATED",
                    },
                ],
                "event_type": "OTHER",
                "subscription": "ONESHOT",
                "evidence": "1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6",
                "evidence_date": "2019-03-11 10:57:45",
                "evidence_file": "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad",
                "evidence_file_date": "2019-03-11 10:57:46",
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
                "closing_date": "2018-06-27 11:40:05",
                "detail": "ASM unit test2",
                "historic_state": [
                    {
                        "analyst": generic_data["global_vars"]["hacker_email"],
                        "date": "2018-06-27 08:00:00",
                        "state": "OPEN",
                    },
                    {
                        "analyst": generic_data["global_vars"]["hacker_email"],
                        "date": "2018-06-27 10:40:05",
                        "state": "CREATED",
                    },
                ],
                "event_type": "OTHER",
                "subscription": "ONESHOT",
                "evidence": "1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6",
                "evidence_date": "2019-03-11 10:57:47",
                "evidence_file": "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad",
                "evidence_file_date": "2019-03-11 10:57:48",
            },
            {
                "project_name": "group1",
                "event_id": "418900973",
                "accessibility": "Repositorio",
                "affected_components": "Otro(s)",
                "analyst": generic_data["global_vars"]["hacker_email"],
                "client": "Fluid",
                "client_project": "group1",
                "closer": "unittest",
                "closing_date": "2018-06-27 10:40:05",
                "detail": "ASM unit test2",
                "historic_state": [
                    {
                        "analyst": generic_data["global_vars"]["hacker_email"],
                        "date": "2018-06-27 09:00:00",
                        "state": "OPEN",
                    },
                    {
                        "analyst": generic_data["global_vars"]["hacker_email"],
                        "date": "2018-06-27 10:30:05",
                        "state": "CREATED",
                    },
                ],
                "event_type": "OTHER",
                "subscription": "ONESHOT",
                "evidence": "1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6",
                "evidence_date": "2019-03-11 10:57:49",
                "evidence_file": "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad",
                "evidence_file_date": "2019-03-11 10:57:50",
            },
            {
                "project_name": "group1",
                "event_id": "418900974",
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
                        "date": "2018-06-27 12:40:05",
                        "state": "CREATED",
                    },
                ],
                "event_type": "OTHER",
                "subscription": "ONESHOT",
                "evidence": "1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6",
                "evidence_date": "2019-03-11 10:57:45",
                "evidence_file": "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad",
                "evidence_file_date": "2019-03-11 10:57:46",
            },
            {
                "project_name": "group1",
                "event_id": "418900975",
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
                        "date": "2018-06-27 12:40:05",
                        "state": "CREATED",
                    },
                ],
                "event_type": "OTHER",
                "subscription": "ONESHOT",
                "evidence": "1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6",
                "evidence_date": "2019-03-11 10:57:45",
                "evidence_file": "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad",
                "evidence_file_date": "2019-03-11 10:57:46",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
