from api.resolvers.git_root import (
    last_state_status_update,
    machine_executions,
    services_toe_lines,
    vulnerabilities,
)
from ariadne import (
    ObjectType,
)

GITROOT: ObjectType = ObjectType("GitRoot")
GITROOT.set_field("lastStateStatusUpdate", last_state_status_update.resolve)
GITROOT.set_field("machineExecutions", machine_executions.resolve)
GITROOT.set_field("servicesToeLines", services_toe_lines.resolve)
GITROOT.set_field("vulnerabilities", vulnerabilities.resolve)

IPROOT: ObjectType = ObjectType("IPRoot")
IPROOT.set_field("vulnerabilities", vulnerabilities.resolve)

URLROOT: ObjectType = ObjectType("URLRoot")
URLROOT.set_field("vulnerabilities", vulnerabilities.resolve)
