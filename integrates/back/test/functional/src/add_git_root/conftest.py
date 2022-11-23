# pylint: disable=import-error
from back.test import (
    db,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_git_root_s3")
@pytest.fixture(autouse=True, scope="session")
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
                last_commit_date="2022-11-02 09:37:57",
                url="https://gitlab.com/fluidattacks/universe",
                commit_count=3,
            ),
        ),
    }

    return await db.populate({**generic_data["db_data"], **data})
