from aioextensions import (
    schedule,
)
from api.mutations import (
    AddRootPayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from batch.dal import (
    generate_key_to_dynamod,
    get_action,
    IntegratesBatchQueue,
    put_action,
)
from batch.enums import (
    Action,
    Product,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.integration_repositories.remove import (
    remove,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from db_model.roots.types import (
    GitRoot,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_white,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import hashlib
from machine.availability import (
    is_check_available,
)
from machine.jobs import (
    FINDINGS,
    queue_job_new,
    SkimsBatchQueue,
)
from mailer import (
    groups as groups_mail,
)
from newutils import (
    logs as logs_utils,
)
from roots import (
    domain as roots_domain,
)
from roots.utils import (
    format_git_repo_url,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_service_white,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> AddRootPayload:
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]
    loaders: Dataloaders = info.context.loaders
    root: GitRoot = await roots_domain.add_git_root(
        loaders, user_email, required_credentials=True, **kwargs
    )
    group_name = root.group_name
    group: Group = await loaders.group.load(group_name)
    if (
        kwargs.get("credentials")
        and (
            result_queue_sync := await roots_domain.queue_sync_git_roots(
                loaders=loaders,
                roots=(root,),
                user_email=user_email,
                group_name=root.group_name,
                queue_with_vpn=kwargs.get("use_vpn", False),
            )
        )
        and (
            result_refresh := await put_action(
                action=Action.REFRESH_TOE_LINES,
                additional_info="*",
                attempt_duration_seconds=7200,
                entity=root.group_name,
                product_name=Product.INTEGRATES,
                subject="integrates@fluidattacks.com",
                queue=IntegratesBatchQueue.SMALL,
                dependsOn=[
                    {
                        "jobId": result_queue_sync.batch_job_id,
                        "type": "SEQUENTIAL",
                    },
                ],
            )
        )
    ):
        await queue_job_new(
            group_name=root.group_name,
            finding_codes=tuple(
                key for key in FINDINGS.keys() if is_check_available(key)
            ),
            queue=SkimsBatchQueue.MEDIUM,
            roots=[root.state.nickname],
            dataloaders=loaders,
            dependsOn=[
                {
                    "jobId": result_refresh.batch_job_id,
                    "type": "SEQUENTIAL",
                },
            ],
        )

        key = generate_key_to_dynamod(
            action_name=Action.UPDATE_ORGANIZATION_OVERVIEW.value,
            additional_info="*",
            entity=group.organization_id,
            subject="integrates@fluidattacks.com",
        )
        overview_action = await get_action(action_dynamo_pk=key)
        if not overview_action:
            await put_action(
                action=Action.UPDATE_ORGANIZATION_OVERVIEW,
                vcpus=2,
                product_name=Product.INTEGRATES,
                queue=IntegratesBatchQueue.SMALL,
                additional_info="*",
                entity=group.organization_id.lower().lstrip("org#"),
                attempt_duration_seconds=7200,
                subject="integrates@fluidattacks.com",
                dependsOn=[
                    {
                        "jobId": result_queue_sync.batch_job_id,
                        "type": "SEQUENTIAL",
                    },
                ],
            )

    await remove(
        repository=OrganizationIntegrationRepository(
            id=hashlib.sha256(kwargs["url"].encode("utf-8")).hexdigest(),
            organization_id=group.organization_id,
            branch=(
                "refs/heads/"
                f'{kwargs["branch"].rstrip().lstrip("refs/heads/")}'
            ),
            last_commit_date=None,
            url=format_git_repo_url(kwargs["url"]),
            commit_count=0,
        )
    )

    schedule(
        groups_mail.send_mail_added_root(
            loaders=loaders,
            branch=root.state.branch,
            environment=root.state.environment,
            group_name=group_name,
            health_check=root.state.includes_health_check,
            root_nickname=root.state.nickname,
            root_url=root.state.url,
            responsible=user_email,
            modified_date=root.state.modified_date,
            vpn_required=root.state.use_vpn,
        )
    )

    logs_utils.cloudwatch_log(
        info.context,
        f'Security: Added a root in {kwargs["group_name"].lower()}',
    )

    return AddRootPayload(root_id=root.id, success=True)
