from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
    set_mocks_return_values,
    set_mocks_side_effects,
)
from dataloaders import (
    apply_context_attrs,
    Dataloaders,
    get_new_context,
)
import pytest
from remove_stakeholder.domain import (
    complete_deletion,
    confirm_deletion_mail,
    remove_stakeholder_all_organizations,
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


@pytest.mark.parametrize(
    ["email"],
    [["unittest2@test.test"]],
)
@patch(MODULE_AT_TEST + "group_access_domain.update", new_callable=AsyncMock)
async def test_confirm_deletion(
    mock_group_access_domain_update: AsyncMock, email: str
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[email]],
        mocked_objects=[mock_group_access_domain_update],
        module_at_test=MODULE_AT_TEST,
        paths_list=["group_access_domain.update"],
    )
    loaders: Dataloaders = get_new_context()
    await confirm_deletion_mail(loaders=loaders, email=email)
    assert mock_group_access_domain_update.called is True


@pytest.mark.parametrize(
    ["email", "modified_by"],
    [["integratesuser@gmail.com", "admin@test.com"]],
)
@patch(MODULE_AT_TEST + "stakeholders_domain.remove", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "orgs_domain.remove_access", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "Dataloaders.stakeholder_organizations_access",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "group_access_domain.remove_access",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "group_access_domain.get_stakeholder_groups_names",
    new_callable=AsyncMock,
)
async def test_remove_stakeholder_all_organizations(
    # pylint: disable=too-many-arguments
    mock_group_access_domain_get_stakeholder_groups_names: AsyncMock,
    mock_group_access_domain_remove_access: AsyncMock,
    mock_dataloaders_stakeholder_organizations_access: AsyncMock,
    mock_orgs_domain_remove_access: AsyncMock,
    mock_stakeholders_domain_remove: AsyncMock,
    email: str,
    modified_by: str,
) -> None:
    mocks_args, mocked_objects, mocked_paths = [
        [[email], [email], [email, modified_by]],
        [
            mock_group_access_domain_get_stakeholder_groups_names,
            mock_group_access_domain_remove_access,
            mock_orgs_domain_remove_access,
        ],
        [
            "group_access_domain.get_stakeholder_groups_names",
            "group_access_domain.remove_access",
            "orgs_domain.remove_access",
        ],
    ]

    assert set_mocks_side_effects(
        mocks_args=mocks_args,
        mocked_objects=mocked_objects,
        module_at_test=MODULE_AT_TEST,
        paths_list=mocked_paths,
    )
    assert set_mocks_return_values(
        mocks_args=[[email], [email]],
        mocked_objects=[
            mock_dataloaders_stakeholder_organizations_access.load,
            mock_stakeholders_domain_remove,
        ],
        module_at_test=MODULE_AT_TEST,
        paths_list=[
            "Dataloaders.stakeholder_organizations_access",
            "stakeholders_domain.remove",
        ],
    )

    await remove_stakeholder_all_organizations(
        email=email, modified_by=modified_by
    )
    assert all(mock_object.called is True for mock_object in mocked_objects)
    assert (
        mock_dataloaders_stakeholder_organizations_access.load.called is True
    )
    assert mock_stakeholders_domain_remove.called is True
