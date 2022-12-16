# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.enrollment.types import (
    Enrollment,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("expire_free_trial")
@pytest.fixture(autouse=True, scope="session")
async def populate() -> bool:
    data = {
        "enrollments": [
            Enrollment(
                email="johndoe@fluidattacks.com",
                enrolled=True,
            ),
        ],
        "stakeholders": [
            Stakeholder(
                email="johndoe@fluidattacks.com",
                first_name="John",
                is_registered=True,
                last_name="Doe",
                registration_date=datetime.fromisoformat(
                    "2022-10-21T15:50:31.280182"
                ),
            ),
            Stakeholder(
                email="janedoe@fluidattacks.com",
                first_name="Jane",
                is_registered=True,
                last_name="Doe",
                registration_date=datetime.fromisoformat(
                    "2022-11-11T14:58:31.280182"
                ),
            ),
            Stakeholder(
                email="uiguaran@fluidattacks.com",
                first_name="Ursula",
                is_registered=True,
                last_name="Iguaran",
                registration_date=datetime.fromisoformat(
                    "2022-11-10T15:58:31.280182"
                ),
            ),
        ],
    }
    return await db.populate(data)
