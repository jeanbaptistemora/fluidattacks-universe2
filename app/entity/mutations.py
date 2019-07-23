from graphene import ObjectType
from app.entity.login import AcceptLegal
from app.entity.resource import (
    AddRepositories, RemoveRepositories,
    AddEnvironments, RemoveEnvironments,
    AddFiles, RemoveFiles, DownloadFile
)
from app.entity.user import (
    GrantUserAccess, RemoveUserAccess,
    EditUser
)
from app.entity.vulnerability import (
    UploadFile, DeleteVulnerability,
    UpdateTreatmentVuln
)
from app.entity.finding import (
    UpdateEvidence, UpdateSeverity,
    UpdateEvidenceDescription,
    AddFindingComment, VerifyFinding, RequestVerification,
    UpdateDescription, UpdateTreatment, DeleteDraft,
    DeleteFinding, ApproveDraft
)
from app.entity.project import (
    AddProjectComment, RemoveTag, AddTags
)
from app.entity.events import UpdateEvent
from app.entity.me import SignIn


class Mutations(ObjectType):
    acceptLegal = AcceptLegal.Field()

    addRepositories = AddRepositories.Field()
    removeRepositories = RemoveRepositories.Field()
    addEnvironments = AddEnvironments.Field()
    removeEnvironments = RemoveEnvironments.Field()
    addFiles = AddFiles.Field()
    removeFiles = RemoveFiles.Field()
    downloadFile = DownloadFile.Field()

    uploadFile = UploadFile.Field()
    updateTreatmentVuln = UpdateTreatmentVuln.Field()
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

    approveDraft = ApproveDraft.Field()
    deleteDraft = DeleteDraft.Field()
    deleteFinding = DeleteFinding.Field()

    updateEvent = UpdateEvent.Field()
    removeTag = RemoveTag.Field()
    addTags = AddTags.Field()

    sign_in = SignIn.Field()
