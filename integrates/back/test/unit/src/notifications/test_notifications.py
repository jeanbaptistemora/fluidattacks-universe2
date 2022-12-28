from dataloaders import (
    Dataloaders,
    get_new_context,
)
from notifications.domain import (
    _get_recipient_first_name_async,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


async def test_recipient_first_name() -> None:
    loaders: Dataloaders = get_new_context()
    email: str = "integratesuser@gmail.com"
    first_name = await _get_recipient_first_name_async(loaders, email)
    assert first_name == "Integrates"
    email_no_name: str = "forces.unittesting@fluidattacks.com"
    first_name = await _get_recipient_first_name_async(loaders, email_no_name)
    assert first_name == email_no_name.split("@", maxsplit=1)[0]
