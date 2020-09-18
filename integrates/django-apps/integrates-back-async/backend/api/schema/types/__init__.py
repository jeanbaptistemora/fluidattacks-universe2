# Standard
from typing import Tuple

# Third party
from ariadne import ObjectType

# Local
from backend.api.schema.types.mutation import MUTATION
from backend.api.schema.types.organization import ORGANIZATION
from backend.api.schema.types.query import QUERY


EVENT = ObjectType('Event')
FINDING = ObjectType('Finding')
FORCES_EXECUTIONS = ObjectType('ForcesExecutions')
INTERNAL_NAME = ObjectType('InternalName')
ME = ObjectType('Me')
PROJECT = ObjectType('Project')
RESOURCE = ObjectType('Resource')
STAKEHOLDER = ObjectType('Stakeholder')
VULNERABILITY = ObjectType('Vulnerability')

TYPES: Tuple[ObjectType, ...] = (
    EVENT,
    FINDING,
    FORCES_EXECUTIONS,
    INTERNAL_NAME,
    ME,
    MUTATION,
    ORGANIZATION,
    PROJECT,
    RESOURCE,
    STAKEHOLDER,
    VULNERABILITY,
    QUERY
)
