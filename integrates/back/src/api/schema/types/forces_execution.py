# None


from api.resolvers.forces_execution import (
    log,
    vulnerabilities,
)
from ariadne import (
    ObjectType,
)

FORCES_EXECUTION = ObjectType("ForcesExecution")
FORCES_EXECUTION.set_field("log", log.resolve)
FORCES_EXECUTION.set_field("vulnerabilities", vulnerabilities.resolve)
