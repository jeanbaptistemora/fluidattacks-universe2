from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
    set_mocks_return_values,
)
from custom_exceptions import (
    OrganizationNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from organizations.utils import (
    get_organization,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["org_id"],
    [["ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"]],
)
@patch(MODULE_AT_TEST + "Dataloaders.organization", new_callable=AsyncMock)
async def test_get_organization(
    mock_dataloaders_organization: AsyncMock,
    org_id: str,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[org_id]],
        mocked_objects=[mock_dataloaders_organization.load],
        module_at_test=MODULE_AT_TEST,
        paths_list=["Dataloaders.organization"],
    )
    loaders: Dataloaders = get_new_context()
    result_org = await get_organization(loaders, org_id)
    assert result_org
    assert result_org.id == org_id


@pytest.mark.parametrize(
    ["org_id_to_raise_exception"],
    [
        ["madeup-org"],
        [
            "ORG#made-up-org-id",
        ],
    ],
)
@patch(MODULE_AT_TEST + "Dataloaders.organization", new_callable=AsyncMock)
async def test_get_organization_exception(
    mock_dataloaders_organization: AsyncMock,
    org_id_to_raise_exception: str,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[org_id_to_raise_exception]],
        mocked_objects=[mock_dataloaders_organization.load],
        module_at_test=MODULE_AT_TEST,
        paths_list=["Dataloaders.organization"],
    )
    loaders: Dataloaders = get_new_context()
    with pytest.raises(OrganizationNotFound) as org_not_found:
        await get_organization(loaders, org_id_to_raise_exception)

    assert (
        str(org_not_found.value) == "Access denied or organization not found"
    )
