# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    HttpsPatSecret,
)
from db_model.enums import (
    CredentialType,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("remove_stakeholder")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data = {
        "credentials": (
            Credentials(
                id="9edc56a8-2743-437e-a6a9-4847b28e1fd5",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="customer_manager@fluidattacks.com",
                state=CredentialsState(
                    modified_by="customer_manager@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-11 11:32:15+00:00"
                    ),
                    name="cred_https_token",
                    type=CredentialType.HTTPS,
                    secret=HttpsPatSecret(token="token test"),
                    is_pat=False,
                ),
            ),
        ),
    }
    return await db.populate({**generic_data["db_data"], **data})
