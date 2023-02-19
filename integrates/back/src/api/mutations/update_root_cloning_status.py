from .payloads.types import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.types import (
    GitRoot,
    RootRequest,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from machine.jobs import (
    FINDINGS,
    queue_job_new,
)
from roots import (
    domain as roots_domain,
)
from typing import (
    Any,
    Optional,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    group_name: str = kwargs["group_name"]
    root_id: str = kwargs["id"]
    commit: Optional[str] = kwargs.get("commit")
    queue_machine: bool = kwargs.get("queue_machine", True)
    root = await loaders.root.load(RootRequest(group_name, root_id))
    if commit is not None and queue_machine and isinstance(root, GitRoot):
        last_commit = await roots_domain.get_commit_last_sucessful_clone(
            loaders=loaders, root=root
        )
        if commit != last_commit:
            await queue_job_new(
                group_name=group_name,
                dataloaders=loaders,
                finding_codes=tuple(FINDINGS.keys()),
                roots=[root.state.nickname],
            )

    await roots_domain.update_root_cloning_status(
        loaders=loaders,
        group_name=group_name,
        root_id=root_id,
        status=GitCloningStatus(kwargs["status"]),
        message=kwargs["message"],
        commit=commit,
    )

    return SimplePayload(success=True)
