from app.app import (
    confirm_deletion,
)
from dataloaders import (
    apply_context_attrs,
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
from settings import (
    TEMPLATES_DIR,
)
from starlette.datastructures import (
    Headers,
)
from starlette.requests import (
    Request,
)
from starlette.routing import (
    Mount,
)
from starlette.staticfiles import (
    StaticFiles,
)
import uuid

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


def create_dummy_simple_session(
    username: str,
    url_token: str,
) -> Request:
    payload = {"url_token": url_token}
    request = Request(
        {
            "type": "http",
            "path": "/confirm_deletion/",
            "http_version": "1.1",
            "method": "GET",
            "path_params": payload,
            "session": dict(username=username, session_key=str(uuid.uuid4())),
            "cookies": {},
            "name": "static",
            "headers": Headers(None).raw,
            "router": Mount(
                "/static",
                StaticFiles(directory=f"{TEMPLATES_DIR}/static"),
                name="static",
            ),
        }
    )
    request = apply_context_attrs(request)

    return request


@pytest.mark.changes_db
async def test_confirm_deletion_mail() -> None:
    email: str = "unittest1@test.test"

    assert await confirm_deletion_mail(email=email)
    assert bool(await get_confirm_deletion(email=email))

    await complete_deletion(loaders=get_new_context(), user_email=email)

    assert not bool(await get_confirm_deletion(email=email))


@pytest.mark.changes_db
async def test_confirm_deletion() -> None:
    email: str = "unittest2@test.test"
    url_token = new_encoded_jwt(
        {
            "user_email": email,
        },
    )

    template = await confirm_deletion(
        create_dummy_simple_session(email, url_token)
    )
    assert "The delete confirmation was Invalid or Expired" in str(
        template.body
    )

    url_token = await confirm_deletion_mail(email=email)
    template = await confirm_deletion(
        create_dummy_simple_session(email, url_token)
    )
    assert "The account deletion was confirmed" in str(template.body)

    template = await confirm_deletion(
        create_dummy_simple_session(email, url_token)
    )
    assert "The delete confirmation was Invalid or Expired" in str(
        template.body
    )
