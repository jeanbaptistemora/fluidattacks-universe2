# Standard
import logging

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.domain import finding as finding_domain
from backend.typing import SimplePayload
from fluidintegrates.settings import LOGGING


logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    evidence_id: str,
    description: str
) -> SimplePayload:
    success = False
    try:
        success = await finding_domain.update_evidence_description(
            finding_id, evidence_id, description
        )
        if success:
            util.queue_cache_invalidation(f'evidence*{finding_id}')
            util.cloudwatch_log(
                info.context,
                (
                    'Security: Evidence description successfully updated in '
                    f'finding {finding_id}'
                )
            )
        else:
            util.cloudwatch_log(
                info.context,
                (
                    'Security: Attempted to update evidence description in '
                    f'{finding_id}'
                )
            )
    except KeyError as ex:
        LOGGER.exception(ex, extra={'extra': locals()})
    return SimplePayload(success=success)
