from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
    set_mocks_return_values,
)
from custom_exceptions import (
    VulnNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)
from vulnerabilities.domain import (
    get_managers_by_size,
    send_treatment_report_mail,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

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
    MODULE_AT_TEST + "group_access_domain.get_managers", new_callable=AsyncMock
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
        mocks_args=mocks_args,
        mocked_objects=mocked_objects,
        paths_list=mocked_paths,
        module_at_test=MODULE_AT_TEST,
    )
    email_managers = await get_managers_by_size(
        get_new_context(), group_name, list_size
    )
    assert list_size == len(email_managers)
    assert all(mock_object.called is True for mock_object in mocked_objects)


@pytest.mark.parametrize(
    [
        "modified_by",
        "justification",
        "vulnerability_id",
        "is_approved",
    ],
    [
        [
            "vulnmanager@gmail.com",
            "test",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
            False,
        ],
    ],
)
@patch(MODULE_AT_TEST + "Dataloaders.vulnerability", new_callable=AsyncMock)
async def test_send_treatment_report_mail_vul_not_found(
    mock_dataloaders_vulnerability: AsyncMock,
    modified_by: str,
    justification: str,
    vulnerability_id: str,
    is_approved: bool,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[vulnerability_id]],
        mocked_objects=[mock_dataloaders_vulnerability.load],
        module_at_test=MODULE_AT_TEST,
        paths_list=["Dataloaders.vulnerability"],
    )
    loaders: Dataloaders = get_new_context()
    with pytest.raises(VulnNotFound):
        await send_treatment_report_mail(
            loaders=loaders,
            modified_by=modified_by,
            justification=justification,
            vulnerability_id=vulnerability_id,
            is_approved=is_approved,
        )
    assert mock_dataloaders_vulnerability.load.called is True
