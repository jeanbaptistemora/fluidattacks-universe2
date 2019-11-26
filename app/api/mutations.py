from graphene import ObjectType
from app.entity.login import AcceptLegal
from app.entity.resource import (
    AddRepositories, UpdateRepositories,
    AddEnvironments, RemoveEnvironments,
    AddResources, UpdateResources,
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
    UpdateEvidence, RemoveEvidence, UpdateSeverity,
    UpdateEvidenceDescription,
    AddFindingComment, VerifyFinding, RequestVerification,
    UpdateDescription, UpdateTreatment, RejectDraft,
    DeleteFinding, ApproveDraft, CreateDraft, SubmitDraft
)
from app.entity.project import (
    AddProjectComment, CreateProject, RemoveTag, AddTags, AddAllProjectAccess,
    RemoveAllProjectAccess
)
from app.entity.event import (
    AddEventComment, CreateEvent, DownloadEventFile, UpdateEvent,
    UpdateEventEvidence
)
from app.entity.me import SignIn, UpdateAccessToken, InvalidateAccessToken
from app.entity.alert import SetAlert
from app.entity.cache import InvalidateCache


class Mutations(ObjectType):
    acceptLegal = AcceptLegal.Field()

    updateAccessToken = UpdateAccessToken.Field()
    invalidateAccessToken = InvalidateAccessToken.Field()

    addRepositories = AddRepositories.Field()
    updateRepositories = UpdateRepositories.Field()
    addEnvironments = AddEnvironments.Field()
    removeEnvironments = RemoveEnvironments.Field()
    addResources = AddResources.Field()
    updateResources = UpdateResources.Field()
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
    removeEvidence = RemoveEvidence.Field()
    updateEvidenceDescription = UpdateEvidenceDescription.Field()

    updateSeverity = UpdateSeverity.Field()

    addAllProjectAccess = AddAllProjectAccess.Field()
    removeAllProjectAccess = RemoveAllProjectAccess.Field()
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

    add_event_comment = AddEventComment.Field()
    create_event = CreateEvent.Field()
    download_event_file = DownloadEventFile.Field()
    update_event = UpdateEvent.Field()
    update_event_evidence = UpdateEventEvidence.Field()

    removeTag = RemoveTag.Field()
    addTags = AddTags.Field()

    setAlert = SetAlert.Field()
    sign_in = SignIn.Field()

    invalidateCache = InvalidateCache.Field()
