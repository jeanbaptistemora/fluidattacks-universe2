from .login import AcceptLegal
from .resource import AddRepositories, RemoveRepositories, AddEnvironments
from graphene import ObjectType

class Mutations(ObjectType):
    acceptLegal = AcceptLegal.Field()

    addRepositories = AddRepositories.Field()

    removeRepositories = RemoveRepositories.Field()

    addEnvironments = AddEnvironments.Field()
