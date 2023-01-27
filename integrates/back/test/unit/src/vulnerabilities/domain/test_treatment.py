from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_mocked_path,
    set_mocks_return_values,
)
from dataloaders import (
    get_new_context,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)
from vulnerabilities.domain import (
    get_managers_by_size,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["group_name", "list_size"],
    [
        ["unittesting", 2],
        ["unittesting", 3],
    ],
)
@patch(
    get_mocked_path("group_access_domain.get_managers"), new_callable=AsyncMock
)
async def test_get_managers_by_size(
    mock_group_access_domain_get_managers: AsyncMock,
    group_name: str,
    list_size: int,
) -> None:
    mocked_objects, mocked_paths, mocks_args = [
        [mock_group_access_domain_get_managers],
        ["group_access_domain.get_managers"],
        [[group_name, list_size]],
    ]

    assert set_mocks_return_values(
        mocked_objects=mocked_objects,
        paths_list=mocked_paths,
        mocks_args=mocks_args,
    )
    email_managers = await get_managers_by_size(
        get_new_context(), group_name, list_size
    )
    assert list_size == len(email_managers)
    assert all(mock_object.called is True for mock_object in mocked_objects)
