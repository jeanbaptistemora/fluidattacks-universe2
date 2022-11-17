# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.roots.enums import (
    RootType,
)
from db_model.roots.types import (
    IPRoot,
    IPRootState,
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
        ],
    }

    return await db.populate({**generic_data["db_data"], **data})
