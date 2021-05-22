# None


from ariadne import ObjectType

from api.resolvers.forces_execution import (
    log,
    vulnerabilities,
)


FORCES_EXECUTION = ObjectType("ForcesExecution")
FORCES_EXECUTION.set_field("log", log.resolve)
FORCES_EXECUTION.set_field("vulnerabilities", vulnerabilities.resolve)
