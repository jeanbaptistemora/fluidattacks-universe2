# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
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
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("update_git_root")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data = {
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.OK,
                    ),
                    created_by=generic_data["global_vars"][
                        "user_manager_email"
                    ],
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="group1",
                    id="88637616-41d4-4242-854a-db8ff7fe1ab6",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment_urls=[],
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by=generic_data["global_vars"][
                            "user_manager_email"
                        ],
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="nickname",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/nickname",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        reason="Cloned successfully",
                        status=GitCloningStatus.OK,
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    group_name="group1",
                    id="9059f0cb-3b55-404b-8fc5-627171f424ad",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment_urls=[],
                        environment="production",
                        gitignore=[],
                        includes_health_check=False,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2022-02-10T14:58:10+00:00"
                        ),
                        nickname="nickname2",
                        other="",
                        reason="",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/nickname2",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
