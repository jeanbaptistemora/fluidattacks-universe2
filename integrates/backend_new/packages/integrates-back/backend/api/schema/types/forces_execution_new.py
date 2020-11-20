# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.new.forces_execution_new import log, vulnerabilities


FORCES_EXECUTION_NEW = ObjectType('ForcesExecutionNew')

FORCES_EXECUTION_NEW.set_field('log', log.resolve)
FORCES_EXECUTION_NEW.set_field('vulnerabilities', vulnerabilities.resolve)
