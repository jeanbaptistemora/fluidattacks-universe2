# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.new.group import (
    stakeholders,
)


GROUP: ObjectType = ObjectType('Project')

GROUP.set_field('stakeholders', stakeholders.resolve)
