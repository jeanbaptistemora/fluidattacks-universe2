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
    UpdateTreatmentVuln, ApproveVulnerability
)
from app.entity.finding import (
    UpdateEvidence, UpdateSeverity,
    UpdateEvidenceDescription,
    AddFindingComment, VerifyFinding, RequestVerification,
    UpdateDescription, UpdateTreatment, RejectDraft,
    DeleteFinding, ApproveDraft, CreateDraft, SubmitDraft
)
from app.entity.project import (
    AddProjectComment, CreateProject, RemoveTag, AddTags
)
from app.entity.event import CreateEvent, UpdateEvent
from app.entity.me import SignIn, UpdateAccessToken, InvalidateAccessToken


class Mutations(ObjectType):
    acceptLegal = AcceptLegal.Field()

    updateAccessToken = UpdateAccessToken.Field()
    invalidateAccessToken = InvalidateAccessToken.Field()

    addRepositories = AddRepositories.Field()
    removeRepositories = RemoveRepositories.Field()
    addEnvironments = AddEnvironments.Field()
    removeEnvironments = RemoveEnvironments.Field()
    addFiles = AddFiles.Field()
    removeFiles = RemoveFiles.Field()
    downloadFile = DownloadFile.Field()

    uploadFile = UploadFile.Field()
    approveVulnerability = ApproveVulnerability.Field()
    updateTreatmentVuln = UpdateTreatmentVuln.Field()
    deleteVulnerability = DeleteVulnerability.Field()

    grantUserAccess = GrantUserAccess.Field()
    removeUserAccess = RemoveUserAccess.Field()
    editUser = EditUser.Field()

    updateEvidence = UpdateEvidence.Field()
    updateEvidenceDescription = UpdateEvidenceDescription.Field()

    updateSeverity = UpdateSeverity.Field()

    addProjectComment = AddProjectComment.Field()
    createProject = CreateProject.Field()
    addFindingComment = AddFindingComment.Field()

    verifyFinding = VerifyFinding.Field()
    requestVerification = RequestVerification.Field()
    updateDescription = UpdateDescription.Field()
    updateTreatment = UpdateTreatment.Field()

    approveDraft = ApproveDraft.Field()
    create_draft = CreateDraft.Field()
    rejectDraft = RejectDraft.Field()
    deleteFinding = DeleteFinding.Field()
    submit_draft = SubmitDraft.Field()

    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()

    removeTag = RemoveTag.Field()
    addTags = AddTags.Field()

    sign_in = SignIn.Field()
