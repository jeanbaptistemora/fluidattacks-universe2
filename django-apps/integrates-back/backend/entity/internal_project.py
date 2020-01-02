from graphene import ObjectType, String
from backend.domain import internal_project as internal_project_domain


class InternalProject(ObjectType):
    project_name = String()

    @staticmethod
    def resolve_project_name(_, info):
        """ Resolve internal project name """
        del info
        return internal_project_domain.get_project_name()
