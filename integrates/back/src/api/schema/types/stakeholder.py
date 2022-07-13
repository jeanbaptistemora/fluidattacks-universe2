from api.resolvers.stakeholder import (
    email,
    first_login,
    groups,
    last_login,
    responsibility,
    role,
)
from ariadne import (
    ObjectType,
)

STAKEHOLDER: ObjectType = ObjectType("Stakeholder")
STAKEHOLDER.set_field("email", email.resolve)
STAKEHOLDER.set_field("groups", groups.resolve)
STAKEHOLDER.set_field("firstLogin", first_login.resolve)
STAKEHOLDER.set_field("lastLogin", last_login.resolve)
STAKEHOLDER.set_field("responsibility", responsibility.resolve)
STAKEHOLDER.set_field("role", role.resolve)
