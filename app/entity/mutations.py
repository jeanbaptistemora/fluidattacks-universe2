from .login import AcceptLegal
from .resource import (
    AddRepositories, RemoveRepositories,
    AddEnvironments, RemoveEnvironments
)

from .user import RemoveUserAccess
from .finding import UploadFile
from graphene import ObjectType

class Mutations(ObjectType):
    acceptLegal = AcceptLegal.Field()

    addRepositories = AddRepositories.Field()

    removeRepositories = RemoveRepositories.Field()

    addEnvironments = AddEnvironments.Field()

    removeEnvironments = RemoveEnvironments.Field()

    removeUserAccess = RemoveUserAccess.Field()

    uploadFile = UploadFile.Field()
