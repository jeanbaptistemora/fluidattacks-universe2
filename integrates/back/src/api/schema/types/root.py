from api.resolvers.git_root import (
    last_state_status_update,
    toe_lines,
)
from ariadne import (
    ObjectType,
)

GITROOT: ObjectType = ObjectType("GitRoot")
GITROOT.set_field("lastStateStatusUpdate", last_state_status_update.resolve)
GITROOT.set_field("toeLines", toe_lines.resolve)
