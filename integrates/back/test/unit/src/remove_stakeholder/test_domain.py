from app.app import (
    confirm_deletion,
)
from app.views.auth import (
    autoenroll_stakeholder,
)
from dataloaders import (
    apply_context_attrs,
    Dataloaders,
    get_new_context,
)
from db_model.group_access.types import (
    GroupAccessMetadataToUpdate,
    GroupAccessState,
    GroupConfirmDeletion,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from group_access import (
    domain as group_access_domain,
)
from newutils.datetime import (
    get_as_epoch,
    get_now_plus_delta,
    get_utc_now,
)
import pytest
from remove_stakeholder.domain import (
    complete_deletion,
    get_confirm_deletion,
    remove_stakeholder_all_organizations,
)
from sessions import (
    domain as sessions_domain,
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
    expiration_time = get_as_epoch(get_now_plus_delta(minutes=5))
    url_token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload={
            "user_email": email,
        },
        subject="starlette_session",
    )
    await group_access_domain.update(
        loaders=get_new_context(),
        email=email,
        group_name="confirm_deletion",
        metadata=GroupAccessMetadataToUpdate(
            confirm_deletion=GroupConfirmDeletion(
                is_used=False, url_token=url_token
            ),
            expiration_time=expiration_time,
            state=GroupAccessState(modified_date=get_utc_now()),
        ),
    )

    return url_token


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
    assert bool(
        await get_confirm_deletion(loaders=get_new_context(), email=email)
    )

    await complete_deletion(email=email)

    assert not bool(
        await get_confirm_deletion(loaders=get_new_context(), email=email)
    )


@pytest.mark.changes_db
async def test_confirm_deletion() -> None:
    email: str = "unittest2@test.test"
    expiration_time = get_as_epoch(get_now_plus_delta(minutes=5))
    url_token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload={
            "user_email": email,
        },
        subject="starlette_session",
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


@pytest.mark.changes_db
async def test_remove_stakeholder() -> None:
    loaders: Dataloaders = get_new_context()
    email: str = "testanewuser@test.test"
    modified_by: str = "admin@test.test"
    await autoenroll_stakeholder(email, "FirstName", "LastName")

    stakeholder: Stakeholder = await loaders.stakeholder.load(email)
    assert stakeholder.email == email
    assert stakeholder.role == "user"

    await remove_stakeholder_all_organizations(
        email=email, modified_by=modified_by
    )
    assert await loaders.stakeholder_subscriptions.load(email) == []
