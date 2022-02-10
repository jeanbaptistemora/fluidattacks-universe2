from api.resolvers.git_root import (
    credentials,
    last_machine_executions,
    last_state_status_update,
    vulnerabilities,
)
from ariadne import (
    ObjectType,
)

GITROOT: ObjectType = ObjectType("GitRoot")
GITROOT.set_field("credentials", credentials.resolve)
GITROOT.set_field("lastMachineExecutions", last_machine_executions.resolve)
GITROOT.set_field("lastStateStatusUpdate", last_state_status_update.resolve)
GITROOT.set_field("vulnerabilities", vulnerabilities.resolve)

IPROOT: ObjectType = ObjectType("IPRoot")
IPROOT.set_field("vulnerabilities", vulnerabilities.resolve)

URLROOT: ObjectType = ObjectType("URLRoot")
URLROOT.set_field("vulnerabilities", vulnerabilities.resolve)
