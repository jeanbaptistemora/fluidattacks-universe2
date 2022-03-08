# pylint: disable=import-error
from batch import (
    roots,
)
from batch.dal import (
    get_actions_by_name,
)
from batch.enums import (
    Action,
)
from batch.types import (
    BatchProcessing,
    CloneResult,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.types import (
    GitRootItem,
)
from newutils.datetime import (
    get_as_epoch,
    get_now,
)
import os
import pytest
from pytest_mock import (
    MockerFixture,
)
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_clone_roots(
    generic_data: Dict[str, Any],
    mock_tmp_repository: str,
    mocker: MockerFixture,
) -> None:
    loaders: Dataloaders = get_new_context()
    root_1: GitRootItem = await loaders.root.load(
        ("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
    )
    assert root_1.cloning.status == GitCloningStatus.FAILED
    assert root_1.cloning.commit is None
    mocker.patch.object(
        roots,
        "ssh_clone_root",
        return_value=CloneResult(
            success=True,
            commit="6d4519f5d5b97235feb65fcbc8af68e8ef9964b3",
            commit_date="12321312",
        ),
    )
    action = BatchProcessing(
        action_name=Action.CLONE_ROOTS.value,
        entity="group1",
        subject=generic_data["global_vars"]["admin_email"],
        time=str(get_as_epoch(get_now())),
        additional_info="nickname2",
        batch_job_id=None,
        queue="spot_soon",
        key="2",
    )
    assert "README.md" in os.listdir(mock_tmp_repository)

    await roots.clone_roots(item=action)
    loaders.root.clear_all()
    root_1 = await loaders.root.load(
        ("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
    )
    assert root_1.cloning.status == GitCloningStatus.OK
    assert root_1.cloning.commit == "6d4519f5d5b97235feb65fcbc8af68e8ef9964b3"

    assert (
        len(
            await get_actions_by_name(
                action_name=Action.EXECUTE_MACHINE.value, entity="group1"
            )
        )
        > 0
    )
    assert (
        len(
            await get_actions_by_name(
                action_name=Action.REFRESH_TOE_LINES.value, entity="group1"
            )
        )
        > 0
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_clone_roots_failed(
    generic_data: Dict[str, Any],
    mock_tmp_repository: str,
    mocker: MockerFixture,
) -> None:
    loaders: Dataloaders = get_new_context()
    root_1: GitRootItem = await loaders.root.load(
        ("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
    )
    assert root_1.cloning.status == GitCloningStatus.OK
    assert root_1.cloning.commit == "6d4519f5d5b97235feb65fcbc8af68e8ef9964b3"
    mocker.patch.object(
        roots,
        "ssh_clone_root",
        return_value=CloneResult(success=False),
    )
    action = BatchProcessing(
        action_name=Action.CLONE_ROOTS.value,
        entity="group1",
        subject=generic_data["global_vars"]["admin_email"],
        time=str(get_as_epoch(get_now())),
        additional_info="nickname2",
        batch_job_id=None,
        queue="spot_soon",
        key="2",
    )
    assert "README.md" in os.listdir(mock_tmp_repository)

    await roots.clone_roots(item=action)
    loaders.root.clear_all()
    root_1 = await loaders.root.load(
        ("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
    )
    assert root_1.cloning.status == GitCloningStatus.FAILED
    assert root_1.cloning.commit is None
