from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    SimplePayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from batch import (
    dal as batch_dal,
    domain as batch_domain,
)
from batch.enums import (
    Action,
    JobStatus,
    Product,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
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
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, **parameters: Any
) -> SimplePayload:
    try:
        group_name = parameters["group_name"]
        user_info = await sessions_domain.get_jwt_content(info.context)
        action = Action.REFRESH_TOE_LINES
        queue = batch_dal.IntegratesBatchQueue.SMALL
        job_payloads = await batch_domain.get_job_payloads(
            queues=[queue],
            statuses=[
                JobStatus.SUBMITTED,
                JobStatus.PENDING,
                JobStatus.RUNNABLE,
                JobStatus.STARTING,
            ],
        )
        current_job_payload = next(
            iter(
                job_payload
                for job_payload in job_payloads
                if job_payload.action_name == action.value
                and job_payload.entity == group_name
            ),
            None,
        )
        if current_job_payload is None:
            await batch_dal.put_action(
                action=action,
                entity=group_name,
                subject=user_info["user_email"],
                additional_info="*",
                queue=queue,
                product_name=Product.INTEGRATES,
            )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Schedule the toe lines refreshing in {group_name} "
            "group successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to schedule the toe lines refreshing in "
            f"{group_name} group",
        )
        raise

    return SimplePayload(success=True)
