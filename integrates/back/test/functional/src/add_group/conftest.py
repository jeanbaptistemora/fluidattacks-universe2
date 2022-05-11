# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.groups.enums import (
    GroupLanguage,
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
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "orgs": [
            {
                "name": "orgtest",
                "id": "40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                "users": [],
                "groups": [
                    "group2",
                    "group3",
                ],
                "policy": {},
            },
        ],
        "groups": [
            {
                "group": Group(
                    description="-",
                    language=GroupLanguage.EN,
                    name="group2",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        modified_by="unknown",
                        modified_date="2020-05-20T22:00:00+00:00",
                        service=GroupService.BLACK,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.ONESHOT,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                ),
            },
            {
                "group": Group(
                    description="-",
                    language=GroupLanguage.EN,
                    name="group3",
                    state=GroupState(
                        has_machine=False,
                        has_squad=False,
                        modified_by="unknown",
                        modified_date="2020-05-20T22:00:00+00:00",
                        service=GroupService.BLACK,
                        status=GroupStateStatus.DELETED,
                        tier=GroupTier.SQUAD,
                        type=GroupSubscriptionType.ONESHOT,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                ),
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
