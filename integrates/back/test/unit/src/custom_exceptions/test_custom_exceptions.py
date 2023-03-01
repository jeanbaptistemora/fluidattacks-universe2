from back.test.unit.src.utils import (  # pylint: disable=import-error
    create_dummy_info,
    create_dummy_session,
)
from custom_exceptions import (
    InvalidSchema,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
import pytest
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
