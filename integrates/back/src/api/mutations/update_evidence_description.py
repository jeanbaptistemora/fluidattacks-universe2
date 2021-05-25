import logging
import logging.config

from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from custom_types import SimplePayload
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from findings import domain as findings_domain
from newutils import logs as logs_utils
from redis_cluster.operations import redis_del_by_deps_soon
from settings import LOGGING


logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_integrates
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    evidence_id: str,
    description: str,
) -> SimplePayload:
    success = False
    try:
        success = await findings_domain.update_evidence_description(
            finding_id, evidence_id, description
        )
        if success:
            info.context.loaders.finding.clear(finding_id)
            redis_del_by_deps_soon(
                "update_evidence_description",
                finding_id=finding_id,
            )
            logs_utils.cloudwatch_log(
                info.context,
                (
                    "Security: Evidence description successfully updated in "
                    f"finding {finding_id}"
                ),
            )
        else:
            logs_utils.cloudwatch_log(
                info.context,
                (
                    "Security: Attempted to update evidence description in "
                    f"{finding_id}"
                ),
            )
    except KeyError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return SimplePayload(success=success)
