# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupFile,
    GroupState,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("resources")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data: Dict[str, Any] = {
        "groups": [
            {
                "group": Group(
                    created_by="unknown",
                    created_date="2020-05-20T22:00:00+00:00",
                    description="-",
                    language=GroupLanguage.EN,
                    name="group1",
                    state=GroupState(
                        has_machine=False,
                        has_squad=False,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date="2020-05-20T22:00:00+00:00",
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    files=[
                        GroupFile(
                            description="Test",
                            file_name="test.zip",
                            modified_by="unittest@fluidattacks.com",
                            modified_date="2019-03-01T20:21+00:00",
                        ),
                        GroupFile(
                            description="Test",
                            file_name="shell.exe",
                            modified_by="unittest@fluidattacks.com",
                            modified_date="2019-04-24T19:56+00:00",
                        ),
                        GroupFile(
                            description="Test",
                            file_name="shell2.exe",
                            modified_by="unittest@fluidattacks.com",
                            modified_date="2019-04-24T19:59+00:00",
                        ),
                        GroupFile(
                            description="Test",
                            file_name="asdasd.py",
                            modified_by="unittest@fluidattacks.com",
                            modified_date="2019-08-06T19:28+00:00",
                        ),
                    ],
                ),
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
