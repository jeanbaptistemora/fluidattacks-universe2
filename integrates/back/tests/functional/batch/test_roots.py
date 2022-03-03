# pylint: disable=import-outside-toplevel
from batch import (
    roots as batch_roots,
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
from roots import (
    domain as roots_domain,
)
from typing import (
    Any,
    Dict,
    Tuple,
)


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

    try:
        await batch_roots.queue_sync_git_roots(
            loaders=loaders,
            user_email=generic_data["global_vars"]["admin_email"],
            roots=(root_1,),
            group_name="group1",
        )
        assert False
    except RootAlreadyCloning:
        assert True


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_no_creds(
    generic_data: Dict[str, Any],
) -> None:
    loaders: Dataloaders = get_new_context()
    root_1: RootItem = await loaders.root.load(
        ("group1", "5059f0cb-4b55-404b-3fc5-627171f424af")
    )

    try:
        await batch_roots.queue_sync_git_roots(
            loaders=loaders,
            user_email=generic_data["global_vars"]["admin_email"],
            roots=(root_1,),
            group_name="group1",
        )
        assert False
    except CredentialNotFound:
        assert True


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_no_valid_root(
    generic_data: Dict[str, Any],
) -> None:
    loaders: Dataloaders = get_new_context()
    root_1: RootItem = await loaders.root.load(
        ("group1", "63298a73-9dff-46cf-b42d-9b2f01a56690")
    )

    try:
        await batch_roots.queue_sync_git_roots(
            loaders=loaders,
            user_email=generic_data["global_vars"]["admin_email"],
            roots=(root_1,),
            group_name="group1",
        )
        assert False
    except InactiveRoot:
        assert True


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
    generic_data: Dict[str, Any], mocker
) -> None:
    mocker.patch.object(
        batch_roots,
        "ssh_ls_remote_root",
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
async def test_queue_sync_git_roots_already_in_queue_running(
    generic_data: Dict[str, Any], mocker
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
                additional_info="nickname1,nickname2,nickname3",
                queue="spot_soon",
                batch_job_id="1",
                running=False,
            ),
        ),
    )

    loaders: Dataloaders = get_new_context()

    try:
        await batch_roots.queue_sync_git_roots(
            loaders=loaders,
            user_email=generic_data["global_vars"]["admin_email"],
            group_name="group1",
        )
        assert False
    except RootAlreadyCloning:
        assert True


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
                    additional_info="nickname1,nickname2,nickname3",
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
                    additional_info="nickname1,nickname2,nickname3",
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
                    additional_info="nickname1,nickname2,nickname3",
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
    mocker,
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
