from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
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
    ["stakeholders_emails", "made_up_email"],
    [
        [
            ["integratesmanager@gmail.com", "integratesuser@gmail.com"],
            "madeupstakeholder@gmail.com",
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "_get_stakeholder_organizations_access",
    new_callable=AsyncMock,
)
async def test_stakeholder_organizations_access_loader(
    mock__get_stakeholder_organizations_access: AsyncMock,
    mocked_data_for_module: Any,
    stakeholders_emails: list,
    made_up_email: str,
) -> None:
    mock__get_stakeholder_organizations_access.side_effect = (
        mocked_data_for_module(
            mock_path="_get_stakeholder_organizations_access",
            mock_args=[stakeholders_emails],
            module_at_test=MODULE_AT_TEST,
        )
    )
    loaders: Dataloaders = get_new_context()
    expected_orgs = [
        "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
        "ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac",  # NOSONAR
        "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86",
        "ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1",  # NOSONAR
    ]
    stakeholder_orgs_access = (
        await loaders.stakeholder_organizations_access.load_many(
            stakeholders_emails
        )
    )
    for stakeholder_access in stakeholder_orgs_access:
        stakeholder_orgs_ids = [
            org_access.organization_id for org_access in stakeholder_access
        ]
        assert sorted(stakeholder_orgs_ids) == expected_orgs

    assert mock__get_stakeholder_organizations_access.call_count == 2

    mock__get_stakeholder_organizations_access.side_effect = (
        mocked_data_for_module(
            mock_path="_get_stakeholder_organizations_access",
            mock_args=[made_up_email],
            module_at_test=MODULE_AT_TEST,
        )
    )
    stakeholder_orgs_access_not_found = (
        await loaders.stakeholder_organizations_access.load(made_up_email)
    )
    assert not stakeholder_orgs_access_not_found
    assert mock__get_stakeholder_organizations_access.call_count == 3
