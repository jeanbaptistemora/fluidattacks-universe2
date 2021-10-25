from back.tests import (
    db,
)
from db_model.roots.types import (
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_event")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: Dict[str, Any]) -> bool:
    data = {
        "roots": (
            GitRootItem(
                cloning=GitRootCloning(
                    modified_date="2020-11-19T13:37:10+00:00",
                    reason="root creation",
                    status="UNKNOWN",
                ),
                group_name="group1",
                id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                machine_execution=None,
                metadata=GitRootMetadata(type="Git"),
                state=GitRootState(
                    branch="master",
                    environment="production",
                    environment_urls=[],
                    git_environment_urls=[],
                    gitignore=[],
                    includes_health_check=True,
                    modified_by="admin@gmail.com",
                    modified_date="2020-11-19T13:37:10+00:00",
                    nickname="nickname",
                    other=None,
                    reason=None,
                    status="ACTIVE",
                    url="https://gitlab.com/fluidattacks/events",
                ),
            ),
        )
    }

    return await db.populate({**generic_data["db_data"], **data})
