# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=import-outside-toplevel
from batch import (
    BatchProcessing,
)
import json
import pytest
from pytest_mock import (
    MockerFixture,
)


@pytest.mark.asyncio
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("mock_pull_namespace_from_s3")
@pytest.mark.usefixtures("test_integrates_session")
async def test_main_empty_configs(
    test_group: str, mocker: MockerFixture
) -> None:
    mocker.patch(
        "batch.get_action",
        return_value=BatchProcessing(
            key="test",
            action_name="execute-machine",
            entity=test_group,
            subject="skims@fluidattacks.com",
            time="test",
            additional_info=json.dumps(
                {"roots": [], "checks": ["F008", "F001"]}
            ),
            queue="small",
        ),
    )
    mocker.patch("batch.set_running", return_value=None)
    mocker.patch("batch.delete_action", return_value=None)

    import batch

    assert await batch.main(action_dynamo_pk="test") is None


@pytest.mark.asyncio
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("mock_pull_namespace_from_s3")
@pytest.mark.usefixtures("test_integrates_session")
async def test_main_with_configs(
    test_group: str, mocker: MockerFixture
) -> None:
    mocker.patch(
        "batch.get_action",
        return_value=BatchProcessing(
            key="test",
            action_name="execute-machine",
            entity=test_group,
            subject="skims@fluidattacks.com",
            time="test",
            additional_info=json.dumps(
                {"roots": ["namespace"], "checks": ["F008", "F001"]}
            ),
            queue="small",
        ),
    )
    mocker.patch("batch.set_running", return_value=None)
    mocker.patch("batch.delete_action", return_value=None)

    import batch

    assert await batch.main(action_dynamo_pk="test") is None


@pytest.mark.asyncio
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("mock_pull_namespace_from_s3")
@pytest.mark.usefixtures("test_integrates_session")
async def test_main_bad_roots(test_group: str, mocker: MockerFixture) -> None:
    mocker.patch(
        "batch.get_action",
        return_value=BatchProcessing(
            key="test",
            action_name="execute-machine",
            entity=test_group,
            subject="skims@fluidattacks.com",
            time="test",
            additional_info=json.dumps(
                {
                    "roots": ["bad_namespace_1", "bad_namespace_2"],
                    "checks": ["F008", "F001"],
                }
            ),
            queue="small",
        ),
    )
    mocker.patch("batch.set_running", return_value=None)
    mocker.patch("batch.delete_action", return_value=None)

    import batch

    assert await batch.main(action_dynamo_pk="test") is None
