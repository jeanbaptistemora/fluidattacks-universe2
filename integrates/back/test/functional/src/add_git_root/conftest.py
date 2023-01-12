# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
import pytest
import pytest_asyncio


@pytest.mark.resolver_test_group("add_git_root")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict) -> bool:
    data: dict = {
        "organization_unreliable_integration_repository": (
            OrganizationIntegrationRepository(
                id=(
                    "62d6130b84736f251d03171352149ce238691c11f3b1535dd"
                    "70fc7a2bfdf77fd"
                ),
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                branch="refs/heads/trunk",
                last_commit_date=datetime.fromisoformat(
                    "2022-11-02T09:37:57+00:00"
                ),
                url="https://gitlab.com/fluidattacks/universe",
                commit_count=3,
            ),
        ),
    }

    return await db.populate({**generic_data["db_data"], **data})
