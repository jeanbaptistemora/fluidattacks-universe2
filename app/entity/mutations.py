from .login import AcceptLegal
from .resource import AddRepositories, RemoveRepositories
from graphene import ObjectType

class Mutations(ObjectType):
    acceptLegal = AcceptLegal.Field()

    addRepositories = AddRepositories.Field()

    removeRepositories = RemoveRepositories.Field()
