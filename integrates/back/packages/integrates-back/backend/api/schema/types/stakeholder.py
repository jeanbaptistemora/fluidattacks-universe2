# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.stakeholder import groups


STAKEHOLDER: ObjectType = ObjectType('Stakeholder')

STAKEHOLDER.set_field('projects', groups.resolve)
