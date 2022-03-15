# pylint: disable=import-error
from batch import (
    roots as batch_roots,
)
from batch.dal import (
    delete_action,
)
from batch.enums import (
    Action,
)
from batch.types import (
    BatchProcessing,
)
from custom_exceptions import (
    CredentialNotFound,
    InactiveRoot,
    RootAlreadyCloning,
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
    RootItem,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from roots.domain import (
    update_root_cloning_status,
)
from typing import (
    Any,
    Dict,
    Tuple,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_real_ssh_ok(
    generic_data: Dict[str, Any]
) -> None:

    loaders: Dataloaders = get_new_context()
    root_1: RootItem = await loaders.root.load(
        ("group1", "6160f0cb-4b66-515b-4fc6-738282f535af")
    )

    result = await batch_roots.queue_sync_git_roots(
        loaders=loaders,
        user_email=generic_data["global_vars"]["admin_email"],
        roots=(root_1,),
        group_name="group1",
    )
    assert result.success
    # restore db state
    if result.dynamo_pk:
        await delete_action(dynamodb_pk=result.dynamo_pk)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_real_https_ok(
    generic_data: Dict[str, Any]
) -> None:

    loaders: Dataloaders = get_new_context()
    root_1: RootItem = await loaders.root.load(
        ("group1", "7271f1cb-5b77-626b-5fc7-849393f646az")
    )

    result = await batch_roots.queue_sync_git_roots(
        loaders=loaders,
        user_email=generic_data["global_vars"]["admin_email"],
        roots=(root_1,),
        group_name="group1",
    )
    assert result.success
    # restore db state
    if result.dynamo_pk:
        await delete_action(dynamodb_pk=result.dynamo_pk)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_real_https_same_commit(
    generic_data: Dict[str, Any], mocker: MockerFixture
) -> None:
    mocker.patch.object(
        batch_roots, "is_in_s3", return_value=("nickname8", True)
    )
    loaders: Dataloaders = get_new_context()
    await update_root_cloning_status(
        loaders,
        "group1",
        "7271f1cb-5b77-626b-5fc7-849393f646az",
        "OK",
        "Success",
        "63afdb8d9cc5230a0137593d20a2fd2c4c73b92b",
    )
    loaders.root.clear_all()
    root_1: RootItem = await loaders.root.load(
        ("group1", "7271f1cb-5b77-626b-5fc7-849393f646az")
    )

    result = await batch_roots.queue_sync_git_roots(
        loaders=loaders,
        user_email=generic_data["global_vars"]["admin_email"],
        roots=(root_1,),
        group_name="group1",
    )
    assert result is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_real_ssh_same_commit(
    generic_data: Dict[str, Any], mocker: MockerFixture
) -> None:
    mocker.patch.object(
        batch_roots, "is_in_s3", return_value=("nickname6", True)
    )
    loaders: Dataloaders = get_new_context()
    await update_root_cloning_status(
        loaders,
        "group1",
        "6160f0cb-4b66-515b-4fc6-738282f535af",
        "OK",
        "Success",
        "63afdb8d9cc5230a0137593d20a2fd2c4c73b92b",
    )
    loaders.root.clear_all()
    root_1: RootItem = await loaders.root.load(
        ("group1", "6160f0cb-4b66-515b-4fc6-738282f535af")
    )

    result = await batch_roots.queue_sync_git_roots(
        loaders=loaders,
        user_email=generic_data["global_vars"]["admin_email"],
        roots=(root_1,),
        group_name="group1",
    )
    assert result is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_already_in_queue_level_selected_roots(
    generic_data: Dict[str, Any], mocker: MockerFixture
) -> None:
    mocker.patch.object(
        batch_roots,
        "get_actions_by_name",
        return_value=(
            BatchProcessing(
                key="1",
                action_name=Action.CLONE_ROOTS.value,
                entity="group1",
                subject=generic_data["global_vars"]["admin_email"],
                time="1",
                additional_info="nickname1",
                queue="spot_soon",
                batch_job_id="1",
                running=False,
            ),
        ),
    )

    loaders: Dataloaders = get_new_context()
    root_1: RootItem = await loaders.root.load(
        ("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
    )

    with pytest.raises(RootAlreadyCloning):
        await batch_roots.queue_sync_git_roots(
            loaders=loaders,
            user_email=generic_data["global_vars"]["admin_email"],
            roots=(root_1,),
            group_name="group1",
        )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_no_creds(
    generic_data: Dict[str, Any],
) -> None:
    loaders: Dataloaders = get_new_context()
    root_1: RootItem = await loaders.root.load(
        ("group1", "5059f0cb-4b55-404b-3fc5-627171f424af")
    )

    with pytest.raises(CredentialNotFound):
        await batch_roots.queue_sync_git_roots(
            loaders=loaders,
            user_email=generic_data["global_vars"]["admin_email"],
            roots=(root_1,),
            group_name="group1",
        )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_no_valid_root(
    generic_data: Dict[str, Any],
) -> None:
    loaders: Dataloaders = get_new_context()
    root_1: RootItem = await loaders.root.load(
        ("group1", "63298a73-9dff-46cf-b42d-9b2f01a56690")
    )

    with pytest.raises(InactiveRoot):
        await batch_roots.queue_sync_git_roots(
            loaders=loaders,
            user_email=generic_data["global_vars"]["admin_email"],
            roots=(root_1,),
            group_name="group1",
        )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_no_queue(
    generic_data: Dict[str, Any],
) -> None:
    loaders: Dataloaders = get_new_context()
    root_1: GitRootItem = await loaders.root.load(
        ("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
    )

    result = await batch_roots.queue_sync_git_roots(
        loaders=loaders,
        user_email=generic_data["global_vars"]["admin_email"],
        roots=(root_1,),
        group_name="group1",
    )
    assert not result
    loaders.root.clear_all()
    root: GitRootItem = await loaders.root.load(
        ("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
    )
    assert root.cloning.status == GitCloningStatus.FAILED


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_cloning(
    generic_data: Dict[str, Any], mocker: MockerFixture
) -> None:
    mocker.patch.object(
        batch_roots,
        "ssh_ls_remote",
        return_value="904d294729ad03fd2dadbb89b920389458e53a61c",
    )
    loaders: Dataloaders = get_new_context()
    root_1: GitRootItem = await loaders.root.load(
        ("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
    )

    result = await batch_roots.queue_sync_git_roots(
        loaders=loaders,
        user_email=generic_data["global_vars"]["admin_email"],
        roots=(root_1,),
        group_name="group1",
    )
    assert result
    loaders.root.clear_all()
    root: GitRootItem = await loaders.root.load(
        ("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
    )
    assert root.cloning.status == GitCloningStatus.CLONING


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_with_same_commit_in_s3(
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(
        batch_roots,
        "ssh_ls_remote",
        return_value="6d2059f5d5b3954feb65fcbc5a368e8ef9964b62",
    )
    mocker.patch.object(
        batch_roots,
        "is_in_s3",
        return_value=("nickname2", True),
    )

    loaders: Dataloaders = get_new_context()
    root_1: GitRootItem = await loaders.root.load(
        ("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
    )

    result = await batch_roots.queue_sync_git_roots(
        loaders=loaders,
        user_email="",
        roots=(root_1,),
        group_name="group1",
    )
    assert not result
    loaders.root.clear_all()
    root: GitRootItem = await loaders.root.load(
        ("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
    )
    assert root.cloning.status == GitCloningStatus.FAILED


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_with_same_commit_not_in_s3(
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(
        batch_roots,
        "ssh_ls_remote",
        return_value="6d2059f5d5b3954feb65fcbc5a368e8ef9964b62",
    )
    mocker.patch.object(
        batch_roots,
        "is_in_s3",
        return_value=("nickname2", False),
    )

    loaders: Dataloaders = get_new_context()
    root_1: GitRootItem = await loaders.root.load(
        ("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
    )

    result = await batch_roots.queue_sync_git_roots(
        loaders=loaders,
        user_email="",
        roots=(root_1,),
        group_name="group1",
    )
    assert result
    loaders.root.clear_all()
    root: GitRootItem = await loaders.root.load(
        ("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
    )
    assert root.cloning.status == GitCloningStatus.CLONING


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_already_in_queue_running(
    generic_data: Dict[str, Any], mocker: MockerFixture
) -> None:
    mocker.patch.object(
        batch_roots,
        "get_actions_by_name",
        return_value=(
            BatchProcessing(
                key="1",
                action_name=Action.CLONE_ROOTS.value,
                entity="group1",
                subject=generic_data["global_vars"]["admin_email"],
                time="1",
                additional_info="nickname1",
                queue="spot_soon",
                batch_job_id="1",
                running=True,
            ),
            BatchProcessing(
                key="1",
                action_name=Action.CLONE_ROOTS.value,
                entity="group1",
                subject=generic_data["global_vars"]["admin_email"],
                time="1",
                additional_info=(
                    "nickname1,nickname2,nickname3,nickname6,nickname8"
                ),
                queue="spot_soon",
                batch_job_id="1",
                running=False,
            ),
        ),
    )

    loaders: Dataloaders = get_new_context()

    with pytest.raises(RootAlreadyCloning):
        await batch_roots.queue_sync_git_roots(
            loaders=loaders,
            user_email=generic_data["global_vars"]["admin_email"],
            group_name="group1",
        )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
@pytest.mark.parametrize(
    "batch_items,must_rise",
    [
        [  # already in queque with provided roots
            (
                BatchProcessing(
                    key="1",
                    action_name=Action.CLONE_ROOTS.value,
                    entity="group1",
                    subject="any",
                    time="1",
                    additional_info=(
                        "nickname1,nickname2,nickname3,nickname6,nickname8"
                    ),
                    queue="spot_soon",
                    batch_job_id="1",
                    running=False,
                ),
            ),
            True,
        ],
        [  # already in queque, no provide roots, by default select all
            (
                BatchProcessing(
                    key="1",
                    action_name=Action.CLONE_ROOTS.value,
                    entity="group1",
                    subject="any",
                    time="1",
                    additional_info=(
                        "nickname1,nickname2,nickname3,nickname6,nickname8"
                    ),
                    queue="spot_soon",
                    batch_job_id="1",
                    running=False,
                ),
            ),
            True,
        ],
        [
            (  # has a running job, a queued job for all roots
                BatchProcessing(
                    key="1",
                    action_name=Action.CLONE_ROOTS.value,
                    entity="group1",
                    subject="any",
                    time="1",
                    additional_info="nickname1",
                    queue="spot_soon",
                    batch_job_id="1",
                    running=True,
                ),
                BatchProcessing(
                    key="1",
                    action_name=Action.CLONE_ROOTS.value,
                    entity="group1",
                    subject="any",
                    time="1",
                    additional_info=(
                        "nickname1,nickname2,nickname3,nickname6,nickname8"
                    ),
                    queue="spot_soon",
                    batch_job_id="1",
                    running=False,
                ),
            ),
            True,
        ],
        [
            (
                BatchProcessing(
                    key="1",
                    action_name=Action.CLONE_ROOTS.value,
                    entity="group1",
                    subject="any",
                    time="1",
                    additional_info="nickname1",
                    queue="spot_soon",
                    batch_job_id="1",
                    running=True,
                ),
            ),
            False,
        ],
        [
            (
                BatchProcessing(
                    key="1",
                    action_name=Action.CLONE_ROOTS.value,
                    entity="group1",
                    subject="any",
                    time="1",
                    additional_info="nickname1,nickname2",
                    queue="spot_soon",
                    batch_job_id="1",
                    running=False,
                ),
            ),
            False,
        ],
    ],
)
async def test_queue_sync_git_roots(
    generic_data: Dict[str, Any],
    mocker: MockerFixture,
    batch_items: Tuple[BatchProcessing, ...],
    must_rise: bool,
) -> None:
    mocker.patch.object(
        batch_roots,
        "get_actions_by_name",
        return_value=batch_items,
    )

    loaders: Dataloaders = get_new_context()

    try:
        await batch_roots.queue_sync_git_roots(
            loaders=loaders,
            user_email=generic_data["global_vars"]["admin_email"],
            group_name="group1",
        )
        assert not must_rise
    except RootAlreadyCloning:
        assert must_rise
