from api.resolvers.git_root import (
    last_state_status_update,
    services_toe_lines,
)
from ariadne import (
    ObjectType,
)

GITROOT: ObjectType = ObjectType("GitRoot")
GITROOT.set_field("lastStateStatusUpdate", last_state_status_update.resolve)
GITROOT.set_field("servicesToeLines", services_toe_lines.resolve)
