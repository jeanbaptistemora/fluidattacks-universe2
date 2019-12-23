from graphene import ObjectType
from backend.entity.login import AcceptLegal
from backend.entity.resource import (
    AddResources, UpdateResources,
    AddFiles, RemoveFiles, DownloadFile
)
from backend.entity.user import (
    GrantUserAccess, RemoveUserAccess,
    EditUser
)
from backend.entity.vulnerability import (
    UploadFile, DeleteVulnerability,
    UpdateTreatmentVuln, ApproveVulnerability
)
from backend.entity.finding import (
    UpdateEvidence, RemoveEvidence, UpdateSeverity,
    UpdateEvidenceDescription,
    AddFindingComment, VerifyFinding, HandleAcceptation, RequestVerification,
    UpdateDescription, UpdateTreatment, RejectDraft,
    DeleteFinding, ApproveDraft, CreateDraft, SubmitDraft
)
from backend.entity.project import (
    AddProjectComment, CreateProject, RemoveProject, RemoveTag, AddTags, AddAllProjectAccess,
    RemoveAllProjectAccess
)
from backend.entity.event import (
    AddEventComment, CreateEvent, DownloadEventFile, SolveEvent, UpdateEvent,
    UpdateEventEvidence, RemoveEventEvidence
)
from backend.entity.me import SignIn, UpdateAccessToken, InvalidateAccessToken
from backend.entity.alert import SetAlert
from backend.entity.cache import InvalidateCache


class Mutations(ObjectType):
    acceptLegal = AcceptLegal.Field()

    updateAccessToken = UpdateAccessToken.Field()
    invalidateAccessToken = InvalidateAccessToken.Field()

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
    removeProject = RemoveProject.Field()
    addFindingComment = AddFindingComment.Field()

    verifyFinding = VerifyFinding.Field()
    handleAcceptation = HandleAcceptation.Field()
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
    remove_event_evidence = RemoveEventEvidence.Field()
    solve_event = SolveEvent.Field()

    removeTag = RemoveTag.Field()
    addTags = AddTags.Field()

    setAlert = SetAlert.Field()
    sign_in = SignIn.Field()

    invalidateCache = InvalidateCache.Field()
