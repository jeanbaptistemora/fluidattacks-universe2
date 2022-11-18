# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("toe_ports")
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
                        modified_date="2020-11-19T13:37:10+00:00",
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
                        address="192.168.1.1",
                        modified_by="admin@gmail.com",
                        modified_date="2020-11-19T13:37:10+00:00",
                        nickname="root2",
                        other=None,
                        port="8081",
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
                attacked_at=datetime.fromisoformat(
                    "2020-01-02T05:00:00+00:00"
                ),
                attacked_by="admin@gmail.com",
                be_present=True,
                be_present_until=None,
                address="192.168.1.1",
                port="8080",
                first_attack_at=datetime.fromisoformat(
                    "2020-01-02T05:00:00+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=True,
                seen_at=datetime.fromisoformat("2000-01-01T05:00:00+00:00"),
                seen_first_time_by="test1@test.com",
                root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
            ),
            ToePort(
                attacked_at=datetime.fromisoformat(
                    "2021-02-11T05:00:00+00:00"
                ),
                attacked_by="admin@gmail.com",
                be_present=False,
                be_present_until=datetime.fromisoformat(
                    "2021-03-11T05:00:00+00:00"
                ),
                address="192.168.1.1",
                port="8081",
                first_attack_at=datetime.fromisoformat(
                    "2021-02-11T05:00:00+00:00"
                ),
                group_name="group1",
                has_vulnerabilities=False,
                seen_at=datetime.fromisoformat("2020-01-11T05:00:00+00:00"),
                seen_first_time_by="test2@test.com",
                root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
