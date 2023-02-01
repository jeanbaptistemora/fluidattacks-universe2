# pylint: disable=import-error
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
    RootAlreadyCloning,
)
from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.types import (
    GitRoot,
    Root,
    RootRequest,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from roots import (
    domain as roots_domain,
)
from roots.domain import (
    update_root_cloning_status,
)
from typing import (
    Any,
    cast,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_real_ssh_ok(
    generic_data: dict[str, Any], mocker: MockerFixture
) -> None:
    mocker.patch.object(roots_domain, "is_in_s3", return_value=False)
    loaders = get_new_context()
    root_1: Root = await loaders.root.load(
        RootRequest("group1", "6160f0cb-4b66-515b-4fc6-738282f535af")
    )

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        user_email=generic_data["global_vars"]["admin_email"],
        roots=(root_1,),  # type: ignore
        group_name="group1",
    )
    assert result.success  # type: ignore
    # restore db state
    if result.dynamo_pk:  # type: ignore
        await delete_action(dynamodb_pk=result.dynamo_pk)  # type: ignore


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_real_https_ok(
    generic_data: dict[str, Any], mocker: MockerFixture
) -> None:
    mocker.patch.object(roots_domain, "is_in_s3", return_value=False)
    loaders = get_new_context()
    root_1: Root = await loaders.root.load(
        RootRequest("group1", "7271f1cb-5b77-626b-5fc7-849393f646az")
    )

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        user_email=generic_data["global_vars"]["admin_email"],
        roots=(root_1,),  # type: ignore
        group_name="group1",
    )
    assert result.success  # type: ignore
    # restore db state
    if result.dynamo_pk:  # type: ignore
        await delete_action(dynamodb_pk=result.dynamo_pk)  # type: ignore


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_real_https_same_commit(
    generic_data: dict[str, Any], mocker: MockerFixture
) -> None:
    mocker.patch.object(roots_domain, "is_in_s3", return_value=True)
    loaders = get_new_context()
    await update_root_cloning_status(
        loaders,
        "group1",
        "7271f1cb-5b77-626b-5fc7-849393f646az",
        GitCloningStatus.OK,
        "Success",
        "63afdb8d9cc5230a0137593d20a2fd2c4c73b92b",
    )
    loaders.root.clear_all()
    root_1: Root = await loaders.root.load(
        RootRequest("group1", "7271f1cb-5b77-626b-5fc7-849393f646az")
    )

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        user_email=generic_data["global_vars"]["admin_email"],
        roots=(root_1,),  # type: ignore
        group_name="group1",
    )
    assert result is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_real_ssh_same_commit(
    generic_data: dict[str, Any], mocker: MockerFixture
) -> None:
    mocker.patch.object(roots_domain, "is_in_s3", return_value=True)
    loaders = get_new_context()
    await update_root_cloning_status(
        loaders,
        "group1",
        "6160f0cb-4b66-515b-4fc6-738282f535af",
        GitCloningStatus.OK,
        "Success",
        "63afdb8d9cc5230a0137593d20a2fd2c4c73b92b",
    )
    loaders.root.clear_all()
    root_1: Root = await loaders.root.load(
        RootRequest("group1", "6160f0cb-4b66-515b-4fc6-738282f535af")
    )

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        user_email=generic_data["global_vars"]["admin_email"],
        roots=(root_1,),  # type: ignore
        group_name="group1",
    )
    assert result is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_already_in_queue_level_selected_roots(
    generic_data: dict[str, Any], mocker: MockerFixture
) -> None:
    mocker.patch.object(
        roots_domain,
        "get_actions_by_name",
        return_value=(
            BatchProcessing(
                key="1",
                action_name=Action.CLONE_ROOTS.value,
                entity="group1",
                subject=generic_data["global_vars"]["admin_email"],
                time="1",
                additional_info=(
                    '{"group_name": "group1", "roots": ["nickname1"]}'
                ),
                queue="small",
                batch_job_id="1",
                running=False,
            ),
        ),
    )
    mocker.patch.object(roots_domain, "is_in_s3", return_value=False)

    loaders = get_new_context()
    root_1: Root = await loaders.root.load(
        RootRequest("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
    )

    with pytest.raises(RootAlreadyCloning):
        await roots_domain.queue_sync_git_roots(
            loaders=loaders,
            user_email=generic_data["global_vars"]["admin_email"],
            roots=(root_1,),  # type: ignore
            group_name="group1",
        )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_no_creds(
    generic_data: dict[str, Any], mocker: MockerFixture
) -> None:
    loaders = get_new_context()
    root_1: Root = await loaders.root.load(
        RootRequest("group1", "5059f0cb-4b55-404b-3fc5-627171f424af")
    )
    mocker.patch.object(roots_domain, "is_in_s3", return_value=False)

    with pytest.raises(CredentialNotFound):
        await roots_domain.queue_sync_git_roots(
            loaders=loaders,
            user_email=generic_data["global_vars"]["admin_email"],
            roots=(root_1,),  # type: ignore
            group_name="group1",
        )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_no_queue(
    generic_data: dict[str, Any], mocker: MockerFixture
) -> None:
    mocker.patch.object(roots_domain, "is_in_s3", return_value=False)

    loaders = get_new_context()
    root_1 = cast(
        GitRoot,
        await loaders.root.load(
            RootRequest("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
        ),
    )

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        user_email=generic_data["global_vars"]["admin_email"],
        roots=(root_1,),
        group_name="group1",
    )
    assert not result
    loaders.root.clear_all()
    root = cast(
        GitRoot,
        await loaders.root.load(
            RootRequest("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
        ),
    )
    assert root.cloning.status == GitCloningStatus.FAILED


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_cloning(
    generic_data: dict[str, Any], mocker: MockerFixture
) -> None:
    mocker.patch.object(roots_domain, "is_in_s3", return_value=False)
    mocker.patch.object(
        roots_domain,
        "ssh_ls_remote",
        return_value="904d294729ad03fd2dadbb89b920389458e53a61c",
    )
    loaders = get_new_context()
    root_1 = cast(
        GitRoot,
        await loaders.root.load(
            RootRequest("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
        ),
    )

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        user_email=generic_data["global_vars"]["admin_email"],
        roots=(root_1,),
        group_name="group1",
    )
    assert result
    loaders.root.clear_all()
    root = cast(
        GitRoot,
        await loaders.root.load(
            RootRequest("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
        ),
    )
    assert root.cloning.status == GitCloningStatus.QUEUED


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_with_same_commit_in_s3(
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(
        roots_domain,
        "ssh_ls_remote",
        return_value="6d2059f5d5b3954feb65fcbc5a368e8ef9964b62",
    )
    mocker.patch.object(
        roots_domain,
        "is_in_s3",
        return_value=True,
    )

    loaders = get_new_context()
    root_1 = cast(
        GitRoot,
        await loaders.root.load(
            RootRequest("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
        ),
    )

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        user_email="",
        roots=(root_1,),
        group_name="group1",
    )
    assert not result
    loaders.root.clear_all()
    root = cast(
        GitRoot,
        await loaders.root.load(
            RootRequest("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
        ),
    )
    assert root.cloning.status == GitCloningStatus.FAILED


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_with_same_commit_not_in_s3(
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(
        roots_domain,
        "ssh_ls_remote",
        return_value="6d2059f5d5b3954feb65fcbc5a368e8ef9964b62",
    )
    mocker.patch.object(
        roots_domain,
        "is_in_s3",
        return_value=False,
    )

    loaders = get_new_context()
    root_1 = cast(
        GitRoot,
        await loaders.root.load(
            RootRequest("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
        ),
    )

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        user_email="",
        roots=(root_1,),
        group_name="group1",
    )
    assert result
    loaders.root.clear_all()
    root = cast(
        GitRoot,
        await loaders.root.load(
            RootRequest("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
        ),
    )
    assert root.cloning.status == GitCloningStatus.QUEUED


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_already_in_queue_running(
    generic_data: dict[str, Any], mocker: MockerFixture
) -> None:
    mocker.patch.object(
        roots_domain,
        "is_in_s3",
        return_value=False,
    )
    mocker.patch.object(
        roots_domain,
        "get_actions_by_name",
        return_value=(
            BatchProcessing(
                key="1",
                action_name=Action.CLONE_ROOTS.value,
                entity="group1",
                subject=generic_data["global_vars"]["admin_email"],
                time="1",
                additional_info=(
                    '{"group_name": "group1", '
                    '"roots": ["nickname1", "nickname2", "nickname3", '
                    '"nickname6", "nickname8"]}'
                ),
                queue="small",
                batch_job_id="1",
                running=False,
            ),
            BatchProcessing(
                key="1",
                action_name=Action.CLONE_ROOTS.value,
                entity="group1",
                subject=generic_data["global_vars"]["admin_email"],
                time="1",
                additional_info=(
                    '{"group_name": "group1", "roots": ["nickname1"]}'
                ),
                queue="small",
                batch_job_id="1",
                running=True,
            ),
        ),
    )

    loaders = get_new_context()
    roots = cast(
        list[GitRoot],
        await loaders.root.load_many(
            [
                RootRequest("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6"),
                RootRequest("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax"),
                RootRequest("group1", "9059f0cb-3b55-404b-8fc5-627171f424ad"),
                RootRequest("group1", "6160f0cb-4b66-515b-4fc6-738282f535af"),
                RootRequest("group1", "7271f1cb-5b77-626b-5fc7-849393f646az"),
            ]
        ),
    )

    with pytest.raises(RootAlreadyCloning):
        await roots_domain.queue_sync_git_roots(
            loaders=loaders,
            user_email=generic_data["global_vars"]["admin_email"],
            group_name="group1",
            roots=tuple(roots),
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
                        '{"group_name": "group1", '
                        '"roots": ["nickname1", "nickname2", "nickname3", '
                        '"nickname6", "nickname8"]}'
                    ),
                    queue="small",
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
                        '{"group_name": "group1", '
                        '"roots": ["nickname1", "nickname2", "nickname3", '
                        '"nickname6", "nickname8"]}'
                    ),
                    queue="small",
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
                    additional_info=(
                        '{"group_name": "group1", '
                        '"roots": ["nickname1", "nickname2", "nickname3", '
                        '"nickname6", "nickname8"]}'
                    ),
                    queue="small",
                    batch_job_id="1",
                    running=False,
                ),
                BatchProcessing(
                    key="1",
                    action_name=Action.CLONE_ROOTS.value,
                    entity="group1",
                    subject="any",
                    time="1",
                    additional_info=(
                        '{"group_name": "group1", "roots": ["nickname1"]}'
                    ),
                    queue="small",
                    batch_job_id="1",
                    running=True,
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
                    additional_info=(
                        '{"group_name": "group1", "roots": ["nickname1"]}'
                    ),
                    queue="small",
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
                    additional_info=(
                        '{"group_name": "group1", '
                        '"roots": ["nickname1", "nickname2"]}'
                    ),
                    queue="small",
                    batch_job_id="1",
                    running=False,
                ),
            ),
            False,
        ],
    ],
)
async def test_queue_sync_git_roots(
    generic_data: dict[str, Any],
    mocker: MockerFixture,
    batch_items: tuple[BatchProcessing, ...],
    must_rise: bool,
) -> None:
    mocker.patch.object(
        roots_domain,
        "is_in_s3",
        return_value=False,
    )
    mocker.patch.object(
        roots_domain,
        "get_actions_by_name",
        return_value=batch_items,
    )

    loaders = get_new_context()
    roots = cast(
        list[GitRoot],
        await loaders.root.load_many(
            [
                RootRequest("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6"),
                RootRequest("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax"),
                RootRequest("group1", "9059f0cb-3b55-404b-8fc5-627171f424ad"),
                RootRequest("group1", "6160f0cb-4b66-515b-4fc6-738282f535af"),
                RootRequest("group1", "7271f1cb-5b77-626b-5fc7-849393f646az"),
            ]
        ),
    )

    try:
        await roots_domain.queue_sync_git_roots(
            loaders=loaders,
            user_email=generic_data["global_vars"]["admin_email"],
            group_name="group1",
            roots=tuple(roots),
        )
        assert not must_rise
    except RootAlreadyCloning:
        assert must_rise
