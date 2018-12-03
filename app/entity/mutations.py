from .login import AcceptLegal
from .resource import (
    AddRepositories, RemoveRepositories,
    AddEnvironments, RemoveEnvironments
)
from .user import (
    GrantUserAccess, RemoveUserAccess,
    EditUser
)
from .vulnerability import (
    UploadFile, DeleteVulnerability
)
from .finding import UpdateEvidence, UpdateSeverity
from graphene import ObjectType

class Mutations(ObjectType):
    acceptLegal = AcceptLegal.Field()

    addRepositories = AddRepositories.Field()

    removeRepositories = RemoveRepositories.Field()

    addEnvironments = AddEnvironments.Field()

    removeEnvironments = RemoveEnvironments.Field()

    removeUserAccess = RemoveUserAccess.Field()

    uploadFile = UploadFile.Field()

    deleteVulnerability = DeleteVulnerability.Field()

    grantUserAccess = GrantUserAccess.Field()

    editUser = EditUser.Field()

    updateEvidence = UpdateEvidence.Field()

    updateSeverity = UpdateSeverity.Field()
