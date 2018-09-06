from .login import AcceptLegal
from .resource import (
    AddRepositories, RemoveRepositories,
    AddEnvironments, RemoveEnvironments
)
from graphene import ObjectType

class Mutations(ObjectType):
    acceptLegal = AcceptLegal.Field()

    addRepositories = AddRepositories.Field()

    removeRepositories = RemoveRepositories.Field()

    addEnvironments = AddEnvironments.Field()

    removeEnvironments = RemoveEnvironments.Field()
