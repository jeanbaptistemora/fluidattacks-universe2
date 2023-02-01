from dataloaders import (
    get_new_context,
)
from db_model.credentials.types import (
    OauthAzureSecret,
)
from organizations.validations import (
    validate_credentials_oauth,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_validate_credentials_oauth() -> None:
    await validate_credentials_oauth(
        loaders=get_new_context(),
        organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
        user_email="unittest@fluidattacks.com",
        secret_type=OauthAzureSecret,
    )
