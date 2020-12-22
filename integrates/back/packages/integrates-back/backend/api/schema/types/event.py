# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.new.event import consulting


EVENT = ObjectType('Event')

EVENT.set_field('consulting', consulting.resolve)
