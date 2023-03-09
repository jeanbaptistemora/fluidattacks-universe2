from collections.abc import (
    Callable,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
import pytest
from typing import (
    Any,
)

MOCKED_DATA: dict[str, dict[str, Any]] = {
    "db_model.organization_access.get._get_stakeholder_organizations_access": {
        '[["integratesmanager@gmail.com", "integratesuser@gmail.com"]]': [
            [
                OrganizationAccess(
                    organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                    email="integratesmanager@gmail.com_testing",
                    expiration_time=None,
                    has_access=None,
                    invitation=None,
                    role="user_manager",
                ),
                OrganizationAccess(
                    organization_id="ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac",
                    email="integratesmanager@gmail.com",
                    expiration_time=None,
                    has_access=None,
                    invitation=None,
                    role="admin",
                ),
                OrganizationAccess(
                    organization_id="ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86",
                    email="integratesmanager@gmail.com",
                    expiration_time=None,
                    has_access=None,
                    invitation=None,
                    role="user",
                ),
                OrganizationAccess(
                    organization_id="ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1",
                    email="integratesmanager@gmail.com",
                    expiration_time=None,
                    has_access=None,
                    invitation=None,
                    role="admin",
                ),
            ],
            [
                OrganizationAccess(
                    organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                    email="integratesuser@gmail.com",
                    expiration_time=None,
                    has_access=None,
                    invitation=None,
                    role="user_manager",
                ),
                OrganizationAccess(
                    organization_id="ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac",
                    email="integratesuser@gmail.com",
                    expiration_time=None,
                    has_access=None,
                    invitation=None,
                    role="user_manager",
                ),
                OrganizationAccess(
                    organization_id="ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86",
                    email="integratesuser@gmail.com",
                    expiration_time=None,
                    has_access=None,
                    invitation=None,
                    role=None,
                ),
                OrganizationAccess(
                    organization_id="ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1",
                    email="integratesuser@gmail.com",
                    expiration_time=None,
                    has_access=None,
                    invitation=None,
                    role="user_manager",
                ),
            ],
        ],
        '["madeupstakeholder@gmail.com"]': [[]],
    },
}


@pytest.fixture
def mocked_data_for_module(
    *,
    resolve_mocked_data: Any,
) -> Any:
    def _mocked_data_for_module(
        mock_path: str, mock_args: list[Any], module_at_test: str
    ) -> Callable[[str, list[Any], str], Any]:
        return resolve_mocked_data(
            mocked_data=MOCKED_DATA,
            mock_path=mock_path,
            mock_args=mock_args,
            module_at_test=module_at_test,
        )

    return _mocked_data_for_module
