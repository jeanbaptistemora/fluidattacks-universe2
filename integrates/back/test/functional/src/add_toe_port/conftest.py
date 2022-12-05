# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.roots.enums import (
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
@pytest.mark.resolver_test_group("add_toe_port")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    test_email = "admin@gmail.com"
    test_date = "2020-11-19T13:37:10+00:00"
    test_status = "ACTIVE"
    data: Dict[str, Any] = {
        "roots": [
            {
                "root": IPRoot(
                    created_by=test_email,
                    created_date=test_date,
                    group_name="group1",
                    id="83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
                    organization_name="orgtest",
                    state=IPRootState(
                        address="192.168.1.1",
                        modified_by=test_email,
                        modified_date=test_date,
                        nickname="ip_1",
                        other=None,
                        port="8080",
                        reason=None,
                        status=test_status,  # type: ignore
                    ),
                    type=RootType.IP,
                ),
                "historic_state": [],
            },
            {
                "root": IPRoot(
                    created_by=test_email,
                    created_date=test_date,
                    group_name="group1",
                    id="83cadbdc-23f3-463a-9421-f50f8d0cb1e6",
                    organization_name="orgtest",
                    state=IPRootState(
                        address="192.168.1.1",
                        modified_by=test_email,
                        modified_date=test_date,
                        nickname="ip_1",
                        other=None,
                        port="8081",
                        reason=None,
                        status=test_status,  # type: ignore
                    ),
                    type=RootType.IP,
                ),
                "historic_state": [],
            },
            {
                "root": IPRoot(
                    created_by=test_email,
                    created_date=test_date,
                    group_name="group1",
                    id="7a9759ad-218a-4a98-9210-31dd78d61580",
                    organization_name="orgtest",
                    state=IPRootState(
                        address="192.168.1.2",
                        modified_by=test_email,
                        modified_date=test_date,
                        nickname="ip_3",
                        other=None,
                        port="8080",
                        reason=None,
                        status=test_status,  # type: ignore
                    ),
                    type=RootType.IP,
                ),
                "historic_state": [],
            },
        ],
        "toe_ports": (
            ToePort(
                attacked_at=datetime.fromisoformat(
                    "2020-01-02T05:00:00+00:00"
                ),
                attacked_by="admin@gmail.com",
                be_present=True,
                be_present_until=None,
                address="192.168.1.2",
                port="8080",
                first_attack_at=datetime.fromisoformat(
                    "2020-01-02T05:00:00+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=True,
                seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
                seen_first_time_by="test1@test.com",
                state=ToePortState(
                    modified_date=datetime.fromisoformat(
                        "2000-01-01T05:00:00+00:00"
                    )
                ),
                root_id="7a9759ad-218a-4a98-9210-31dd78d61580",
            ),
        ),
    }

    return await db.populate({**generic_data["db_data"], **data})
