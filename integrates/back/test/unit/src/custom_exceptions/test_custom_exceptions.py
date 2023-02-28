from back.test.unit.src.utils import (  # pylint: disable=import-error
    create_dummy_info,
    create_dummy_session,
)
from custom_exceptions import (
    InvalidNumberAcceptances,
    InvalidRange,
    InvalidSchema,
    UnableToSendSms,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    VulnerabilityTreatment,
)
from decimal import (
    Decimal,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
from newutils.vulnerabilities import (
    range_to_list,
)
import pytest
from sms.common import (
    send_sms_notification,
)
from twilio.base.exceptions import (
    TwilioRestException,
)
from typing import (
    Any,
)
from unittest import (
    mock,
)
from unittest.mock import (
    AsyncMock,
)
import uuid
from vulnerabilities.domain import (
    validate_accepted_treatment_change,
)
from vulnerability_files.domain import (
    validate_file_schema,
)
import yaml

pytestmark = [
    pytest.mark.asyncio,
]

BUCKET_NAME = "unit_test_bucket"
TABLE_NAME = "integrates_vms"


@mock.patch(
    "dynamodb.operations.get_table_resource",
    new_callable=AsyncMock,
)
async def test_validate_number_acceptances(
    mock_table_resource: AsyncMock,
    dynamo_resource: ServiceResource,
) -> None:
    def mock_query(**kwargs: Any) -> Any:
        return dynamo_resource.Table(TABLE_NAME).query(**kwargs)

    mock_table_resource.return_value.query.side_effect = mock_query
    historic_treatment = [
        VulnerabilityTreatment(
            modified_date=datetime.fromisoformat("2020-01-01T17:00:00+00:00"),
            status=VulnerabilityTreatmentStatus.ACCEPTED,
            accepted_until=datetime.fromisoformat("2020-02-01T17:00:00+00:00"),
            justification="Justification to accept the finding",
            modified_by="unittest@fluidattacks.com",
        ),
        VulnerabilityTreatment(
            modified_date=datetime.fromisoformat("2020-02-01T17:00:00+00:00"),
            status=VulnerabilityTreatmentStatus.UNTREATED,
        ),
    ]
    finding_severity = Decimal("3.0")
    accepted_until = (datetime.now() + timedelta(days=10)).astimezone(
        tz=timezone.utc
    )
    with pytest.raises(InvalidNumberAcceptances):
        await validate_accepted_treatment_change(
            loaders=get_new_context(),
            accepted_until=accepted_until,
            finding_severity=finding_severity,
            group_name="kurome",
            historic_treatment=historic_treatment,
        )
    assert mock_table_resource.called is True


def test_invalid_range_to_list() -> None:
    bad_range_value = "13-12"
    with pytest.raises(InvalidRange):
        assert range_to_list(bad_range_value)


@mock.patch(
    "dynamodb.operations.get_table_resource",
    new_callable=AsyncMock,
)
async def test_validate_file_schema_invalid(
    mock_table_resource: AsyncMock,
    dynamo_resource: ServiceResource,
) -> None:
    def mock_update_item(**kwargs: Any) -> Any:
        return dynamo_resource.Table(TABLE_NAME).update_item(**kwargs)

    mock_table_resource.return_value.update_item.side_effect = mock_update_item
    finding_id = "463461507"
    request = await create_dummy_session("unittest@fluidattacks.com")
    info = create_dummy_info(request)
    # FP: the generated filename is unpredictable
    file_url = (  # NOSONAR
        f"/tmp/vulnerabilities-{uuid.uuid4()}-{finding_id}.yaml"
    )
    with open(file_url, "w", encoding="utf-8") as stream:
        yaml.safe_dump("", stream)
    with pytest.raises(InvalidSchema):  # NOQA
        validate_file_schema(file_url, info)


@mock.patch(
    "dynamodb.operations.get_resource",
    new_callable=AsyncMock,
)
async def test_stakeholder_not_found(
    mock_resource: AsyncMock,
    dynamo_resource: ServiceResource,
) -> None:
    def mock_batch_get_item(**kwargs: Any) -> Any:
        return dynamo_resource.batch_get_item(**kwargs)

    mock_resource.return_value.batch_get_item.side_effect = mock_batch_get_item
    email: str = "testanewuser@test.test"
    loaders: Dataloaders = get_new_context()
    assert not await loaders.stakeholder.load(email)
    assert mock_resource.called is True


async def test_exception_unable_to_send_sms() -> None:
    status = 500
    uri = "/Accounts/ACXXXXXXXXXXXXXXXXX/Messages.json"
    test_phone_number = "12345678"
    test_message = "This is a test message"
    with mock.patch("sms.common.FI_ENVIRONMENT", "production"):
        with mock.patch("sms.common.client.messages.create") as mock_twilio:
            mock_twilio.side_effect = TwilioRestException(status, uri)
            with pytest.raises(UnableToSendSms):
                await send_sms_notification(
                    phone_number=test_phone_number,
                    message_body=test_message,
                )
