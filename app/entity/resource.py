""" GraphQL Entity for Project Resources """
# pylint: disable=F0401
from app.dao import integrates_dao
from graphene import ObjectType, JSONString

class Resource(ObjectType):

    repositories = JSONString()
    environments = JSONString()

    def __init__(self, project_name):
        """ Resource class """
        self.repositories = []
        self.environments = []

        project_info = integrates_dao.get_project_dynamo(project_name)
        for info in project_info:
            if "repositories" in info:
                self.repositories = info['repositories']

            if "environments" in info:
                self.environments = info['environments']

    def resolve_repositories(self, info):
        """ Resolve repositories of the given project """
        del info
        return self.repositories

    def resolve_environments(self, info):
        """ Resolve environments of the given project """
        del info
        return self.environments
