# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.new.finding import (
    consulting,
    observations
)


FINDING = ObjectType('Finding')

FINDING.set_field('consulting', consulting.resolve)
FINDING.set_field('observations', observations.resolve)
