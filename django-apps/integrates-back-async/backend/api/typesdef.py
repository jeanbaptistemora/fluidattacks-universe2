# pylint: disable=import-error

from ariadne import ObjectType

ALERT = ObjectType('Alert')
EVENT = ObjectType('Event')
FINDING = ObjectType('Finding')
FORCES_EXECUTIONS = ObjectType('ForcesExecutions')
INTERNAL_PROJECT_NAME = ObjectType('InternalProject')
ME = ObjectType('Me')
PROJECT = ObjectType('Project')
RESOURCE = ObjectType('Resource')
USER = ObjectType('User')

TYPES = [
    ALERT, EVENT, FINDING, FORCES_EXECUTIONS, INTERNAL_PROJECT_NAME,
    ME, PROJECT, RESOURCE, USER
]
