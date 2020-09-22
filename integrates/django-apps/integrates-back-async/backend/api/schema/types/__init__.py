# Standard
from typing import Tuple

# Third party
from ariadne import ObjectType

# Local
from backend.api.schema.types.group import GROUP
from backend.api.schema.types.mutation import MUTATION
from backend.api.schema.types.organization import ORGANIZATION
from backend.api.schema.types.query import QUERY
from backend.api.schema.types.stakeholder import STAKEHOLDER


EVENT = ObjectType('Event')
FINDING = ObjectType('Finding')
FORCES_EXECUTIONS = ObjectType('ForcesExecutions')
INTERNAL_NAME = ObjectType('InternalName')
ME = ObjectType('Me')
RESOURCE = ObjectType('Resource')
VULNERABILITY = ObjectType('Vulnerability')

TYPES: Tuple[ObjectType, ...] = (
    EVENT,
    FINDING,
    FORCES_EXECUTIONS,
    GROUP,
    INTERNAL_NAME,
    ME,
    MUTATION,
    ORGANIZATION,
    RESOURCE,
    STAKEHOLDER,
    VULNERABILITY,
    QUERY
)
