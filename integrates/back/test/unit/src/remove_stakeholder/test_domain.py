from app.app import (
    confirm_deletion,
)
from app.views.auth import (
    autoenroll_stakeholder,
)
from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
    set_mocks_return_values,
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
from unittest.mock import (
    AsyncMock,
    patch,
)
import uuid

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

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


@pytest.mark.parametrize(
    ["email"],
    [["unittest@test.com"]],
)
@patch(
    MODULE_AT_TEST + "remove_stakeholder_all_organizations",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "group_access_model.remove", new_callable=AsyncMock)
async def test_complete_deletion(
    mock_group_access_model_remove: AsyncMock,
    mock_remove_stakeholder_all_organizations: AsyncMock,
    email: str,
) -> None:
    mocked_objects, mocked_paths, mocks_args = [
        [
            mock_group_access_model_remove,
            mock_remove_stakeholder_all_organizations,
        ],
        ["group_access_model.remove", "remove_stakeholder_all_organizations"],
        [[email], [email]],
    ]
    assert set_mocks_return_values(
        mocks_args=mocks_args,
        mocked_objects=mocked_objects,
        module_at_test=MODULE_AT_TEST,
        paths_list=mocked_paths,
    )
    await complete_deletion(email=email)
    assert all(mock_object.called is True for mock_object in mocked_objects)


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

    stakeholder = await loaders.stakeholder.load(email)
    assert stakeholder
    assert stakeholder.email == email
    assert stakeholder.role == "user"

    await remove_stakeholder_all_organizations(
        email=email, modified_by=modified_by
    )
    assert await loaders.stakeholder_subscriptions.load(email) == []
