from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_module_at_test,
    set_mocks_return_values,
)
from billing.domain import (
    customer_payment_methods,
    get_document_link,
    remove_file,
    save_file,
    search_file,
)
from billing.types import (
    PaymentMethod,
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
import os
import pytest
from starlette.datastructures import (
    UploadFile,
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
    ("organization", "expected_result"),
    (
        (
            Organization(
                created_by="unknown@unknown.com",
                created_date=datetime.fromisoformat(
                    "2018-02-08T00:43:18+00:00"
                ),
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
            [
                PaymentMethod(
                    id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                    fingerprint="",
                    last_four_digits="",
                    expiration_month="",
                    expiration_year="",
                    brand="",
                    default=False,
                    business_name="Fluid",
                    city="Medellín",
                    country="Colombia",
                    email="test@fluidattacks.com",
                    state="Antioquia",
                    rut=None,
                    tax_id=None,
                ),
                PaymentMethod(
                    id="4722b0b7-cfeb-4898-8308-185dfc2523bc",
                    fingerprint="",
                    last_four_digits="",
                    expiration_month="",
                    expiration_year="",
                    brand="",
                    default=False,
                    business_name="Testing Company and Sons",
                    city="Medellín",
                    country="Colombia",
                    email="test@fluidattacks.com",
                    state="Antioquia",
                    rut=None,
                    tax_id=None,
                ),
            ],
        ),
    ),
)
async def test_customer_payment_methods(
    organization: Organization, expected_result: list
) -> None:

    result = await customer_payment_methods(org=organization)
    assert result == expected_result


@pytest.mark.parametrize(
    ("organization", "payment_id", "file_name", "expected_result"),
    (
        (
            Organization(
                created_by="unknown@unknown.com",
                created_date=datetime.fromisoformat(
                    "2018-02-08T00:43:18+00:00"
                ),
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
            "4722b0b7-cfeb-4898-8308-185dfc2523bc",
            "test_file.pdf",
            "https://s3.amazonaws.com/integrates/johndoeatfluid-test-unit/"
            "resources/billing/okada/testing%20company%20and%20sons/"
            "test_file.pdf?X-Amz-Algorithm=TestX-Amz-Credential=Testus-east-1"
            "%2Fs3%2Faws4_request&X-Amz-Date=20230117T170631Z&X-Amz-Expires=10"
            "&X-Amz-SignedHeaders=host&X-Amz-Security-Token=TestX-Amz-"
            "Signature=Test",
        ),
    ),
)
@patch(MODULE_AT_TEST + "s3_ops.sign_url", new_callable=AsyncMock)
async def test_get_document_link(
    mock_s3_ops_sign_url: AsyncMock,
    organization: Organization,
    payment_id: str,
    file_name: str,
    expected_result: str,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[organization.name, payment_id, file_name]],
        mocked_objects=[mock_s3_ops_sign_url],
        module_at_test=MODULE_AT_TEST,
        paths_list=["s3_ops.sign_url"],
    )
    result = await get_document_link(organization, payment_id, file_name)
    assert mock_s3_ops_sign_url.called is True
    assert result == expected_result


@pytest.mark.parametrize(
    ["file_name"],
    [
        ["billing-test-file.png"],
        ["unittesting-test-file.csv"],
    ],
)
@patch(MODULE_AT_TEST + "s3_ops.upload_memory_file", new_callable=AsyncMock)
async def test_save_file(
    mock_s3_ops_upload_memory_file: AsyncMock, file_name: str
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[file_name]],
        mocked_objects=[mock_s3_ops_upload_memory_file],
        module_at_test=MODULE_AT_TEST,
        paths_list=["s3_ops.upload_memory_file"],
    )

    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/resources/" + file_name)
    with open(file_location, "rb") as data:
        test_file = UploadFile(data)  # type: ignore
        await save_file(test_file, file_name)
    mock_s3_ops_upload_memory_file.assert_called_with(
        test_file, f"resources/{file_name}"
    )


@pytest.mark.parametrize(
    ["file_name"],
    [
        ["billing-test-file.png"],
        ["unittesting-test-file.csv"],
    ],
)
@patch(MODULE_AT_TEST + "s3_ops.list_files", new_callable=AsyncMock)
async def test_search_file(
    mock_s3_ops_list_files: AsyncMock, file_name: str
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[file_name]],
        mocked_objects=[mock_s3_ops_list_files],
        module_at_test=MODULE_AT_TEST,
        paths_list=["s3_ops.list_files"],
    )

    assert file_name in await search_file(file_name)
    mock_s3_ops_list_files.assert_called_with(f"resources/{file_name}")


@pytest.mark.parametrize(
    ["file_name"],
    [
        ["billing-test-file.png"],
        ["unittesting-test-file.csv"],
    ],
)
@patch(MODULE_AT_TEST + "s3_ops.remove_file", new_callable=AsyncMock)
async def test_remove_file(
    mock_s3_ops_remove_file: AsyncMock, file_name: str
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[file_name]],
        mocked_objects=[mock_s3_ops_remove_file],
        module_at_test=MODULE_AT_TEST,
        paths_list=["s3_ops.remove_file"],
    )

    await remove_file(file_name)
    mock_s3_ops_remove_file.assert_called_with(f"resources/{file_name}")
