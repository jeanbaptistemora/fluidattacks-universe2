from graphene import ObjectType
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
from .finding import (
    UpdateEvidence, UpdateSeverity,
    UpdateEvidenceDescription,
    AddFindingComment, VerifyFinding, RequestVerification,
    UpdateDescription, UpdateTreatment
)
from .project import AddProjectComment


class Mutations(ObjectType):
    acceptLegal = AcceptLegal.Field()

    addRepositories = AddRepositories.Field()
    removeRepositories = RemoveRepositories.Field()
    addEnvironments = AddEnvironments.Field()
    removeEnvironments = RemoveEnvironments.Field()

    uploadFile = UploadFile.Field()
    deleteVulnerability = DeleteVulnerability.Field()

    grantUserAccess = GrantUserAccess.Field()
    removeUserAccess = RemoveUserAccess.Field()
    editUser = EditUser.Field()

    updateEvidence = UpdateEvidence.Field()
    updateEvidenceDescription = UpdateEvidenceDescription.Field()

    updateSeverity = UpdateSeverity.Field()

    addProjectComment = AddProjectComment.Field()
    addFindingComment = AddFindingComment.Field()

    verifyFinding = VerifyFinding.Field()
    requestVerification = RequestVerification.Field()
    updateDescription = UpdateDescription.Field()
    updateTreatment = UpdateTreatment.Field()
