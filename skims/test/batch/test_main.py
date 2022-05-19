# pylint: disable=import-outside-toplevel,broad-except
from batch import (
    BatchProcessing,
    main as batch_main,
)
from integrates.dal import (
    get_finding_vulnerabilities,
    get_group_findings,
)
import json
from model import (
    core_model,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Dict,
)
from zone import (
    t,
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
            queue="unlimited_spot",
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
            queue="unlimited_spot",
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
            queue="unlimited_spot",
        ),
    )
    mocker.patch("batch.set_running", return_value=None)
    mocker.patch("batch.delete_action", return_value=None)

    import batch

    assert await batch.main(action_dynamo_pk="test") is None


@pytest.mark.asyncio
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("mock_pull_git_repo_initial_commit")
@pytest.mark.usefixtures("test_integrates_session")
async def test_mock_git_report(test_group: str, mocker: MockerFixture) -> None:
    mocker.patch(
        "batch.get_action",
        return_value=BatchProcessing(
            key="test",
            action_name="execute-machine",
            entity=test_group,
            subject="customer@domain.com",
            time="test",
            additional_info=json.dumps(
                {
                    "roots": ["dynamic_namespace_1"],
                    "checks": ["F073"],
                }
            ),
            queue="unlimited_spot",
        ),
    )
    mocker.patch("batch.set_running", return_value=None)
    mocker.patch("batch.delete_action", return_value=None)

    findings = await get_group_findings(group=test_group)
    assert not any(finding.title.startswith("073") for finding in findings)

    await batch_main(action_dynamo_pk="test")

    findings = await get_group_findings(group=test_group)
    assert any(finding.title.startswith("073") for finding in findings)


@pytest.mark.asyncio
@pytest.mark.skims_test_group("functional")
@pytest.mark.skip(reason="Fixing")
@pytest.mark.usefixtures("mock_pull_repo_next_commit")
@pytest.mark.usefixtures("test_integrates_session")
async def test_rebase_no_change_line(
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
                {
                    "roots": ["namespace4"],
                    "checks": ["F099"],
                }
            ),
            queue="unlimited_spot",
        ),
    )
    mocker.patch("batch.set_running", return_value=None)
    mocker.patch("batch.delete_action", return_value=None)
    titles_to_finding: Dict[str, core_model.FindingEnum] = {
        t(finding.value.title): finding for finding in core_model.FindingEnum
    }

    findings = await get_group_findings(group=test_group)
    finding_id = "6ca298ce-8306-4f0d-9db9-103aa92d89d6"
    for finding in findings:
        if (
            finding.title.startswith("099")
            and finding.identifier == finding_id
        ):
            title = finding.title

    import batch

    assert await batch.main(action_dynamo_pk="test") is None

    vulns_before_rebase: EphemeralStore = await get_finding_vulnerabilities(
        finding=titles_to_finding[title],
        finding_id=finding_id,
    )
    for item in vulns_before_rebase.iterate():
        if (
            item.integrates_metadata.uuid
            == "a487943a-a23e-4da5-a693-1b2dbb6ee5a1"
        ):
            where = item.where

    assert where == "4"
