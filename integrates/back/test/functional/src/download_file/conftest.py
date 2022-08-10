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
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("download_file")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "groups": [
            {
                "group": Group(
                    description="-",
                    language=GroupLanguage.EN,
                    name="group1",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date="2020-05-20T22:00:00+00:00",
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    sprint_start_date="2022-06-06T00:00:00",
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
                            modified_date="2019-03-01T19:56+00:00",
                        ),
                        GroupFile(
                            description="Test",
                            file_name="shell2.exe",
                            modified_by="unittest@fluidattacks.com",
                            modified_date="2019-03-01T19:59+00:00",
                        ),
                        GroupFile(
                            description="Test",
                            file_name="asdasd.py",
                            modified_by="unittest@fluidattacks.com",
                            modified_date="2019-03-01T19:59+00:00",
                        ),
                    ],
                ),
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
