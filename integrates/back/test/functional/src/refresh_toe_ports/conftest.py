# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    IPRoot,
    IPRootState,
)
from db_model.toe_ports.types import (
    ToePort,
    ToePortState,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("refresh_toe_ports")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "roots": [
            {
                "root": IPRoot(
                    created_by="admin@gmail.com",
                    created_date="2020-11-19T13:37:10+00:00",
                    group_name="group1",
                    id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    organization_name="orgtest",
                    state=IPRootState(
                        address="192.168.1.1",
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="root1",
                        other=None,
                        port="8080",
                        reason=None,
                        status=RootStatus.ACTIVE,
                    ),
                    type=RootType.IP,
                ),
                "historic_state": [],
            },
            {
                "root": IPRoot(
                    created_by="admin@gmail.com",
                    created_date="2020-11-19T13:37:10+00:00",
                    group_name="group1",
                    id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                    organization_name="orgtest",
                    state=IPRootState(
                        address="192.168.1.2",
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="root2",
                        other=None,
                        port="8081",
                        reason=None,
                        status=RootStatus.INACTIVE,
                    ),
                    type=RootType.IP,
                ),
                "historic_state": [],
            },
        ],
        "toe_ports": (
            ToePort(
                address="192.168.1.1",
                port="8080",
                group_name="group1",
                root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
                seen_first_time_by="test1@test.com",
                state=ToePortState(
                    attacked_at=datetime.fromisoformat(
                        "2020-01-02T05:00:00+00:00"
                    ),
                    attacked_by="admin@gmail.com",
                    be_present=True,
                    be_present_until=None,
                    first_attack_at=datetime.fromisoformat(
                        "2020-01-02T05:00:00+00:00"
                    ),
                    has_vulnerabilities=True,
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2021-01-01T05:00:00+00:00"
                    ),
                ),
            ),
            ToePort(
                address="192.168.1.1",
                port="8081",
                group_name="group1",
                root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
                seen_first_time_by="test1@test.com",
                state=ToePortState(
                    attacked_at=datetime.fromisoformat(
                        "2020-01-02T05:00:00+00:00"
                    ),
                    attacked_by="admin@gmail.com",
                    be_present=False,
                    be_present_until=datetime.fromisoformat(
                        "2021-01-01T05:00:00+00:00"
                    ),
                    first_attack_at=datetime.fromisoformat(
                        "2020-01-02T05:00:00+00:00"
                    ),
                    has_vulnerabilities=True,
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2021-01-01T05:00:00+00:00"
                    ),
                ),
            ),
            ToePort(
                address="192.168.1.2",
                port="8080",
                group_name="group1",
                root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                seen_at=datetime.fromisoformat("2020-01-11T05:00:00+00:00"),
                seen_first_time_by="test2@test.com",
                state=ToePortState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-11T05:00:00+00:00"
                    ),
                    attacked_by="admin@gmail.com",
                    be_present=True,
                    be_present_until=None,
                    first_attack_at=datetime.fromisoformat(
                        "2021-02-11T05:00:00+00:00"
                    ),
                    has_vulnerabilities=False,
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2020-01-11T05:00:00+00:00"
                    ),
                ),
            ),
            ToePort(
                address="192.168.1.2",
                port="8081",
                group_name="group1",
                root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                seen_at=datetime.fromisoformat("2020-01-11T05:00:00+00:00"),
                seen_first_time_by="test2@test.com",
                state=ToePortState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-11T05:00:00+00:00"
                    ),
                    attacked_by="admin@gmail.com",
                    be_present=False,
                    be_present_until=datetime.fromisoformat(
                        "2021-03-11T05:00:00+00:00"
                    ),
                    first_attack_at=datetime.fromisoformat(
                        "2021-02-11T05:00:00+00:00"
                    ),
                    has_vulnerabilities=False,
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2021-01-11T05:00:00+00:00"
                    ),
                ),
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
