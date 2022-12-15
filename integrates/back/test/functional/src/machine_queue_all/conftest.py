from back.test import (  # pylint: disable=import-error
    db,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
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
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationState,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
)
from db_model.types import (
    Policies,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("machine_queue_all")
@pytest.fixture(scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "groups": [
            {
                "group": Group(
                    created_by="customeradmin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-31T21:00:00+00:00"
                    ),
                    description="Test group with Machine services",
                    language=GroupLanguage.EN,
                    name="machinegroup",
                    organization_id="fd672241-f99d-4f19-961c-3c7dd80be47c",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="customeradmin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-31T21:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                )
            },
            {
                "group": Group(
                    created_by="customeradmin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-31T21:00:00+00:00"
                    ),
                    description="Test group with Squad services",
                    language=GroupLanguage.EN,
                    name="squadgroup",
                    organization_id="fd672241-f99d-4f19-961c-3c7dd80be47c",
                    state=GroupState(
                        has_machine=False,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="customeradmin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-31T21:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                )
            },
            {
                "group": Group(
                    created_by="customeradmin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-31T21:00:00+00:00"
                    ),
                    description="Test group with Machine services",
                    language=GroupLanguage.EN,
                    name="deletedgroup",
                    organization_id="fd672241-f99d-4f19-961c-3c7dd80be47c",
                    state=GroupState(
                        has_machine=True,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="customeradmin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-31T21:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.DELETED,
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                )
            },
        ],
        "organizations": [
            {
                "organization": Organization(
                    created_by="customeradmin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-31T21:00:00+00:00"
                    ),
                    id="fd672241-f99d-4f19-961c-3c7dd80be47c",
                    name="testorganization",
                    policies=Policies(
                        modified_by="customeradmin@gmail.com",
                        modified_date="2022-10-31T21:00:00+00:00",
                    ),
                    state=OrganizationState(
                        modified_by="customeradmin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-31T21:00:00+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                )
            }
        ],
        "roots": [
            {
                "historic_state": [],
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-10-31T21:00:00+00:00"
                        ),
                        reason="Clone failed",
                        status=GitCloningStatus.FAILED,
                    ),
                    created_by="customeradmin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-31T21:00:00+00:00"
                    ),
                    group_name="machinegroup",
                    id="0946d6c0-f3ec-4e3e-8281-3681e5c09909",
                    organization_name="testorganization",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        includes_health_check=False,
                        modified_by="customeradmin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-31T21:00:00+00:00"
                        ),
                        nickname="failedroot",
                        status=RootStatus.ACTIVE,
                        url=(
                            "https://gitserver/testorganization/failedroot.git"
                        ),
                    ),
                    type=RootType.GIT,
                ),
            },
            {
                "historic_state": [],
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-10-31T21:00:00+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.OK,
                    ),
                    created_by="customeradmin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-31T21:00:00+00:00"
                    ),
                    group_name="machinegroup",
                    id="3017530c-9923-4aa2-b22e-3b0e7a5f1ac2",
                    organization_name="testorganization",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        includes_health_check=False,
                        modified_by="customeradmin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-31T21:00:00+00:00"
                        ),
                        nickname="inactiveroot",
                        status=RootStatus.INACTIVE,
                        url=(
                            "https://gitserver/testorganization/"
                            "inactiveroot.git"
                        ),
                    ),
                    type=RootType.GIT,
                ),
            },
            {
                "historic_state": [],
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-10-31T21:00:00+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.OK,
                    ),
                    created_by="customeradmin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-31T21:00:00+00:00"
                    ),
                    group_name="machinegroup",
                    id="8a02ba03-e81e-4d45-a0f5-82ed507da6d3",
                    organization_name="testorganization",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        includes_health_check=False,
                        modified_by="customeradmin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-31T21:00:00+00:00"
                        ),
                        nickname="activeroot",
                        status=RootStatus.ACTIVE,
                        url=(
                            "https://gitserver/testorganization/activeroot.git"
                        ),
                    ),
                    type=RootType.GIT,
                ),
            },
            {
                "historic_state": [],
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-10-31T21:00:00+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.OK,
                    ),
                    created_by="customeradmin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-10-31T21:00:00+00:00"
                    ),
                    group_name="squadgroup",
                    id="4fce481b-074d-433d-b894-123cbb323f97",
                    organization_name="testorganization",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        includes_health_check=False,
                        modified_by="customeradmin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-10-31T21:00:00+00:00"
                        ),
                        nickname="activesquadroot",
                        status=RootStatus.ACTIVE,
                        url=(
                            "https://gitserver/testorganization/"
                            "activesquadroot.git"
                        ),
                    ),
                    type=RootType.GIT,
                ),
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
