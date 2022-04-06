from dataloaders import (
    get_new_context,
)
from group_access import (
    domain as group_access_domain,
)
from newutils.datetime import (
    get_as_epoch,
    get_now_plus_delta,
)
from newutils.token import (
    new_encoded_jwt,
)
import pytest
from remove_user.domain import (
    complete_deletion,
    get_confirm_deletion,
)

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


async def confirm_deletion_mail(
    *,
    email: str,
) -> str:
    success = False
    expiration_time = get_as_epoch(get_now_plus_delta(weeks=1))
    url_token = new_encoded_jwt(
        {
            "user_email": email,
        },
    )
    success = await group_access_domain.update(
        email,
        "confirm_deletion",
        {
            "expiration_time": expiration_time,
            "confirm_deletion": {
                "is_used": False,
                "url_token": url_token,
            },
        },
    )
    if success:
        return url_token

    return ""


@pytest.mark.changes_db
async def test_confirm_deletion_mail() -> None:
    email: str = "unittest1@test.test"

    assert await confirm_deletion_mail(email=email)
    assert bool(await get_confirm_deletion(email=email))

    await complete_deletion(loaders=get_new_context(), user_email=email)

    assert not bool(await get_confirm_deletion(email=email))
