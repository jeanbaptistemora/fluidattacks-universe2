from graphene import ObjectType, String

from backend.decorators import (
    get_entity_cache
)

# pylint: disable=super-init-not-called


class BreakBuildExecutions(ObjectType):
    """ GraphQL Entity for the Break Build Executions """
    project_name = String()

    def __init__(self, project_name):
        self.project_name = project_name

    def __str__(self):
        return f'BreakBuildExecutions({self.project_name})'

    @get_entity_cache
    def resolve_project_name(self, info):
        """ Resolve the project_name """
        del info
        return self.project_name
