# pylint: disable=import-outside-toplevel,broad-except
from batch import (
    BatchProcessing,
)
import json
import pytest
from pytest_mock import (
    MockerFixture,
)


@pytest.mark.asyncio
@pytest.mark.skims_test_group("unittesting")
async def test_main_no_action(mocker: MockerFixture) -> None:
    mocker.patch("batch.get_action", return_value=None)

    import batch

    try:
        await batch.main(action_dynamo_pk="test")
        assert False  # this must throws an exception
    except Exception as exc:
        assert "No jobs were found for the key test" in str(exc)


@pytest.mark.asyncio
@pytest.mark.skims_test_group("unittesting")
async def test_main_bad_action(mocker: MockerFixture) -> None:
    mocker.patch(
        "batch.get_action",
        return_value=BatchProcessing(
            key="test",
            action_name="bad-action",
            entity="test",
            subject="test",
            time="test",
            additional_info="test",
            queue="test",
        ),
    )

    import batch

    try:
        await batch.main(action_dynamo_pk="test")
        assert False  # this must throws an exception
    except Exception as exc:
        assert "Invalid action name" in str(exc)


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
            queue="skims_all_later",
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
            queue="skims_all_later",
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
            queue="skims_all_later",
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
async def test_main_bad_group(mocker: MockerFixture) -> None:
    mocker.patch(
        "batch.get_action",
        return_value=BatchProcessing(
            key="test",
            action_name="execute-machine",
            entity="bad_group",
            subject="skims@fluidattacks.com",
            time="test",
            additional_info=json.dumps(
                {
                    "roots": ["bad_namespace_1", "bad_namespace_2"],
                    "checks": ["F008", "F001"],
                }
            ),
            queue="skims_all_later",
        ),
    )
    mocker.patch("batch.set_running", return_value=None)
    mocker.patch("batch.delete_action", return_value=None)

    import batch

    try:
        assert await batch.main(action_dynamo_pk="test") is None
        assert False  # must throws Type error, the group can not be foundd
    except Exception as exc:
        assert isinstance(exc, TypeError)
