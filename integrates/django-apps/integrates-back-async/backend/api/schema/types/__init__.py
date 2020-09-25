# Standard
from typing import Tuple

# Third party
from ariadne import ObjectType

# Local
from backend.api.schema.types.event import EVENT
from backend.api.schema.types.finding import FINDING
from backend.api.schema.types.forces_executions import FORCES_EXECUTIONS
from backend.api.schema.types.group import GROUP
from backend.api.schema.types.internal_name import INTERNAL_NAME
from backend.api.schema.types.me import ME
from backend.api.schema.types.mutation import MUTATION
from backend.api.schema.types.organization import ORGANIZATION
from backend.api.schema.types.query import QUERY
from backend.api.schema.types.resource import RESOURCE
from backend.api.schema.types.stakeholder import STAKEHOLDER
from backend.api.schema.types.vulnerability import VULNERABILITY


TYPES: Tuple[ObjectType, ...] = (
    EVENT,
    FINDING,
    FORCES_EXECUTIONS,
    GROUP,
    INTERNAL_NAME,
    ME,
    MUTATION,
    ORGANIZATION,
    QUERY,
    RESOURCE,
    STAKEHOLDER,
    VULNERABILITY
)
