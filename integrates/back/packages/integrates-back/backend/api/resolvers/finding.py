# pylint:disable=too-many-lines
import logging
import sys
from typing import Any, Union

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from backend.typing import (
    SimplePayload as SimplePayloadType,
    SimpleFindingPayload as SimpleFindingPayloadType,
    ApproveDraftPayload as ApproveDraftPayloadType,
    AddConsultPayload as AddConsultPayloadType,
)
from backend import util
from back.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case  # type: ignore
def resolve_finding_mutation(
        obj: Any,
        info: GraphQLResolveInfo,
        **parameters: Any
) -> Union[
    SimpleFindingPayloadType,
    SimplePayloadType,
    AddConsultPayloadType,
    ApproveDraftPayloadType
]:
    """Resolve findings mutation."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return resolver_func(obj, info, **parameters)
