from collections.abc import (
    Callable,
)
from datetime import (
    datetime,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationDocuments,
    OrganizationPaymentMethods,
    OrganizationState,
)
from db_model.types import (
    Policies,
)
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
)

MOCKED_DATA: dict[str, dict[str, Any]] = {
    "db_model.organizations.get._get_organization_by_id": {
        '["ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"]': Organization(
            created_by="unknown@unknown.com",
            created_date=datetime.fromisoformat("2018-02-08T00:43:18+00:00"),
            id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            name="okada",
            policies=Policies(
                modified_date=datetime.fromisoformat(
                    "2019-11-22T20:07:57+00:00"
                ),
                modified_by="integratesmanager@gmail.com",
                inactivity_period=90,
                max_acceptance_days=60,
                max_acceptance_severity=Decimal("10.0"),
                max_number_acceptances=2,
                min_acceptance_severity=Decimal("0.0"),
                min_breaking_severity=Decimal("0"),
                vulnerability_grace_period=0,
            ),
            state=OrganizationState(
                status=OrganizationStateStatus.ACTIVE,
                modified_by="unknown",
                modified_date=datetime.fromisoformat(
                    "2018-02-08T00:43:18+00:00"
                ),
                pending_deletion_date=datetime.fromisoformat(
                    "2019-11-22T20:07:57+00:00"
                ),
            ),
            country="Colombia",
            payment_methods=[
                OrganizationPaymentMethods(
                    id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                    business_name="Fluid",
                    email="test@fluidattacks.com",
                    country="Colombia",
                    state="Antioquia",
                    city="Medellín",
                    documents=OrganizationDocuments(rut=None, tax_id=None),
                ),
                OrganizationPaymentMethods(
                    id="4722b0b7-cfeb-4898-8308-185dfc2523bc",
                    business_name="Testing Company and Sons",
                    email="test@fluidattacks.com",
                    country="Colombia",
                    state="Antioquia",
                    city="Medellín",
                    documents=OrganizationDocuments(rut=None, tax_id=None),
                ),
            ],
            billing_customer=None,
            vulnerabilities_url=None,
        ),
    },
    "db_model.organizations.get._get_organization_by_name": {
        '["okada"]': Organization(
            created_by="unknown@unknown.com",
            created_date=datetime.fromisoformat("2018-02-08T00:43:18+00:00"),
            id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            name="okada",
            policies=Policies(
                modified_date=datetime.fromisoformat(
                    "2019-11-22T20:07:57+00:00"
                ),
                modified_by="integratesmanager@gmail.com",
                inactivity_period=90,
                max_acceptance_days=60,
                max_acceptance_severity=Decimal("10.0"),
                max_number_acceptances=2,
                min_acceptance_severity=Decimal("0.0"),
                min_breaking_severity=Decimal("0"),
                vulnerability_grace_period=0,
            ),
            state=OrganizationState(
                status=OrganizationStateStatus.ACTIVE,
                modified_by="unknown",
                modified_date=datetime.fromisoformat(
                    "2018-02-08T00:43:18+00:00"
                ),
                pending_deletion_date=datetime.fromisoformat(
                    "2019-11-22T20:07:57+00:00"
                ),
            ),
            country="Colombia",
            payment_methods=[
                OrganizationPaymentMethods(
                    id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                    business_name="Fluid",
                    email="test@fluidattacks.com",
                    country="Colombia",
                    state="Antioquia",
                    city="Medellín",
                    documents=OrganizationDocuments(rut=None, tax_id=None),
                ),
                OrganizationPaymentMethods(
                    id="4722b0b7-cfeb-4898-8308-185dfc2523bc",
                    business_name="Testing Company and Sons",
                    email="test@fluidattacks.com",
                    country="Colombia",
                    state="Antioquia",
                    city="Medellín",
                    documents=OrganizationDocuments(rut=None, tax_id=None),
                ),
            ],
            billing_customer=None,
            vulnerabilities_url=None,
        ),
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
