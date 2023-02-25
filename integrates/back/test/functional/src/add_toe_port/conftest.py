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
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("add_toe_port")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    test_email = "admin@gmail.com"
    data: dict[str, Any] = {
        "roots": [
            {
                "root": IPRoot(
                    created_by=test_email,
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
                    organization_name="orgtest",
                    state=IPRootState(
                        address="192.168.1.1",
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="ip_1",
                        other=None,
                        reason=None,
                        status=RootStatus.ACTIVE,
                    ),
                    type=RootType.IP,
                ),
                "historic_state": [],
            },
            {
                "root": IPRoot(
                    created_by=test_email,
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="83cadbdc-23f3-463a-9421-f50f8d0cb1e6",
                    organization_name="orgtest",
                    state=IPRootState(
                        address="192.168.1.1",
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="ip_1",
                        other=None,
                        reason=None,
                        status=RootStatus.ACTIVE,
                    ),
                    type=RootType.IP,
                ),
                "historic_state": [],
            },
            {
                "root": IPRoot(
                    created_by=test_email,
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="7a9759ad-218a-4a98-9210-31dd78d61580",
                    organization_name="orgtest",
                    state=IPRootState(
                        address="192.168.1.2",
                        modified_by=test_email,
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="ip_3",
                        other=None,
                        reason=None,
                        status=RootStatus.ACTIVE,
                    ),
                    type=RootType.IP,
                ),
                "historic_state": [],
            },
        ],
        "toe_ports": (
            ToePort(
                address="192.168.1.2",
                port="8080",
                group_name="group1",
                seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
                seen_first_time_by="test1@test.com",
                root_id="7a9759ad-218a-4a98-9210-31dd78d61580",
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
                    modified_date=datetime.fromisoformat(
                        "2000-01-01T05:00:00+00:00"
                    ),
                    modified_by="admin@gmail.com",
                ),
            ),
        ),
    }

    return await db.populate({**generic_data["db_data"], **data})
