from ariadne import ObjectType

EVENT = ObjectType('Event')
FINDING = ObjectType('Finding')
FORCES_EXECUTIONS = ObjectType('ForcesExecutions')
INTERNAL_NAME = ObjectType('InternalName')
ME = ObjectType('Me')
PROJECT = ObjectType('Project')
RESOURCE = ObjectType('Resource')
STAKEHOLDER = ObjectType('Stakeholder')
VULNERABILITY = ObjectType('Vulnerability')

TYPES = [
    EVENT, FINDING, FORCES_EXECUTIONS, INTERNAL_NAME,
    ME, PROJECT, RESOURCE, STAKEHOLDER, VULNERABILITY
]
