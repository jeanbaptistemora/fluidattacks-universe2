from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_mocked_path,
    set_mocks_return_values,
)
from forces.domain import (
    is_forces_user,
    update_token,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    [
        "email",
        "expected_result",
    ],
    [
        ["forces.unittesting@fluidattacks.com", True],
        ["unittesting@fluidattacks.com", False],
    ],
)
def test_is_forces_user(email: str, expected_result: bool) -> None:
    result = is_forces_user(email)
    assert result == expected_result


@pytest.mark.parametrize(
    [
        "group_name",
        "organization_id",
        "token",
    ],
    [
        [
            "unittesting",
            "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            "mock_token",
        ],
    ],
)
@patch(
    get_mocked_path("groups_domain.update_metadata"), new_callable=AsyncMock
)
async def test_update_secret_token(
    mock_groups_domain_update_metadata: AsyncMock,
    group_name: str,
    organization_id: str,
    token: str,
) -> None:
    mocked_objects, mocked_paths, mocks_args = [
        [mock_groups_domain_update_metadata],
        ["groups_domain.update_metadata"],
        [[group_name, token, organization_id]],
    ]
    assert set_mocks_return_values(
        mocked_objects=mocked_objects,
        paths_list=mocked_paths,
        mocks_args=mocks_args,
    )

    await update_token(group_name, organization_id, token)
    assert all(mock_object.called is True for mock_object in mocked_objects)
