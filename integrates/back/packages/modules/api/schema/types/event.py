# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from api.resolvers.event import consulting


EVENT = ObjectType('Event')
EVENT.set_field('consulting', consulting.resolve)
