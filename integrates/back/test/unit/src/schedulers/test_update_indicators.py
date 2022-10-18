# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
    get_new_context,
)
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource as ServiceResource,
)
import pytest
from schedulers.update_indicators import (
    create_weekly_date,
    get_date_last_vulns,
)
from typing import (
    Any,
)
from unittest import (
    mock,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_date_last_vulns(dynamo_resource: ServiceResource) -> None:
    def mock_query(**kwargs: Any) -> Any:
        table_name = "integrates_vms"
        return dynamo_resource.Table(table_name).query(**kwargs)

    loaders: Dataloaders = get_new_context()
    finding_id = "422286126"
    with mock.patch(
        "dynamodb.operations.get_table_resource", new_callable=mock.AsyncMock
    ) as mock_table_resource:
        mock_table_resource.return_value.query.side_effect = mock_query
        vulns = await loaders.finding_vulnerabilities.load(finding_id)
    test_data = get_date_last_vulns(vulns)
    expected_output = "2020-09-07 16:01:26"
    assert test_data == expected_output


def test_create_weekly_date() -> None:
    first_date = "2019-09-19 13:23:32"
    test_data = create_weekly_date(first_date)
    expected_output = "Sep 16 - 22, 2019"
    assert test_data == expected_output