# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
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
    GroupState,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("remove_group_tag")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "groups": [
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="-",
                    language=GroupLanguage.EN,
                    name="group1",
                    state=GroupState(
                        has_machine=False,
                        has_squad=False,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tags={
                            "test1",
                            "test2",
                            "test3",
                            "test4",
                            "test5",
                            "test6",
                        },
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                ),
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
