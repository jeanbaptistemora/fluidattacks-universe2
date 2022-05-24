# pylint: disable=import-outside-toplevel
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
@pytest.mark.usefixtures("mock_pull_git_repo_next_commit")
@pytest.mark.usefixtures("test_integrates_session")
async def test_rebase_change_line(
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
                    "roots": ["dynamic_namespace_1"],
                    "checks": ["F073"],
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

    for finding in findings:
        if finding.title.startswith("073"):
            title = finding.title
            finding_id = finding.identifier

    vulns_before_rebase: EphemeralStore = await get_finding_vulnerabilities(
        finding=titles_to_finding[title],
        finding_id=finding_id,
    )
    vulns_before_length = len(vulns_before_rebase)
    for item in vulns_before_rebase.iterate():
        if item.where == "2":
            vuln_1_id = item.integrates_metadata.uuid
        elif item.where == "17":
            vuln_2_id = item.integrates_metadata.uuid

    assert vuln_1_id is not None and vuln_2_id is not None

    await batch_main(action_dynamo_pk="test")

    vulns_after_rebase: EphemeralStore = await get_finding_vulnerabilities(
        finding=titles_to_finding[title],
        finding_id=finding_id,
    )

    assert len(vulns_after_rebase) == vulns_before_length

    for item in vulns_after_rebase.iterate():
        if item.integrates_metadata.uuid == vuln_1_id:
            final_where_1 = item.where
        elif item.integrates_metadata.uuid == vuln_2_id:
            final_where_2 = item.where

    assert final_where_1 == "11" and final_where_2 == "26"
