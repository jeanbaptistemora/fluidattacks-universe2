# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from api.resolvers.tag import groups


TAG = ObjectType('Tag')
TAG.set_field('projects', groups.resolve)
