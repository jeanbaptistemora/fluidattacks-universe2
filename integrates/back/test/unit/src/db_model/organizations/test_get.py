from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
)
from db_model.organizations.get import (
    _get_organization,
)
import pytest
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["org_id", "org_name"],
    [["ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3", "okada"]],
)
@patch(MODULE_AT_TEST + "_get_organization_by_name", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "_get_organization_by_id", new_callable=AsyncMock)
async def test__get_organization(
    mock___get_organization_by_id: AsyncMock,
    mock___get_organization_by_name: AsyncMock,
    mocked_data_for_module: Any,
    org_id: str,
    org_name: str,
) -> None:
    mock___get_organization_by_id.return_value = mocked_data_for_module(
        mock_path="_get_organization_by_id",
        mock_args=[org_id],
        module_at_test=MODULE_AT_TEST,
    )
    org_by_id = await _get_organization(organization_key=org_id)
    assert org_by_id
    assert org_by_id.id == org_id
    assert org_by_id.name == org_name
    assert mock___get_organization_by_id.call_count == 1

    mock___get_organization_by_name.return_value = mocked_data_for_module(
        mock_path="_get_organization_by_name",
        mock_args=[org_name],
        module_at_test=MODULE_AT_TEST,
    )
    org_by_name = await _get_organization(organization_key=org_name)
    assert org_by_name
    assert org_by_name.id == org_id
    assert org_by_name.name == org_name
    assert mock___get_organization_by_name.call_count == 1
