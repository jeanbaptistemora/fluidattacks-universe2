from db_model.events.enums import (
    EventEvidenceId,
    EventSolutionReason,
    EventType,
)

IMAGE_EVIDENCE_IDS = {
    EventEvidenceId.IMAGE_1,
    EventEvidenceId.IMAGE_2,
    EventEvidenceId.IMAGE_3,
    EventEvidenceId.IMAGE_4,
    EventEvidenceId.IMAGE_5,
    EventEvidenceId.IMAGE_6,
}
FILE_EVIDENCE_IDS = {
    EventEvidenceId.FILE_1,
}
SOLUTION_REASON_BY_EVENT_TYPE = {
    EventType.AUTHORIZATION_SPECIAL_ATTACK: {
        EventSolutionReason.PERMISSION_DENIED,
        EventSolutionReason.PERMISSION_GRANTED,
    },
    EventType.CLIENT_CANCELS_PROJECT_MILESTONE: {
        EventSolutionReason.OTHER,
    },
    EventType.CLIENT_EXPLICITLY_SUSPENDS_PROJECT: {
        EventSolutionReason.IS_OK_TO_RESUME,
        EventSolutionReason.AFFECTED_RESOURCE_REMOVED_FROM_SCOPE,
        EventSolutionReason.OTHER,
    },
    EventType.CLONING_ISSUES: {
        EventSolutionReason.AFFECTED_RESOURCE_REMOVED_FROM_SCOPE,
        EventSolutionReason.CLONED_SUCCESSFULLY,
    },
    EventType.CREDENTIAL_ISSUES: {
        EventSolutionReason.AFFECTED_RESOURCE_REMOVED_FROM_SCOPE,
        EventSolutionReason.CREDENTIALS_ARE_WORKING_NOW,
        EventSolutionReason.NEW_CREDENTIALS_PROVIDED,
    },
    EventType.DATA_UPDATE_REQUIRED: {
        EventSolutionReason.AFFECTED_RESOURCE_REMOVED_FROM_SCOPE,
        EventSolutionReason.DATA_UPDATED,
        EventSolutionReason.OTHER,
    },
    EventType.ENVIRONMENT_ISSUES: {
        EventSolutionReason.AFFECTED_RESOURCE_REMOVED_FROM_SCOPE,
        EventSolutionReason.ENVIRONMENT_IS_WORKING_NOW,
        EventSolutionReason.NEW_ENVIRONMENT_PROVIDED,
    },
    EventType.INSTALLER_ISSUES: {
        EventSolutionReason.AFFECTED_RESOURCE_REMOVED_FROM_SCOPE,
        EventSolutionReason.INSTALLER_IS_WORKING_NOW,
        EventSolutionReason.OTHER,
    },
    EventType.MISSING_SUPPLIES: {
        EventSolutionReason.AFFECTED_RESOURCE_REMOVED_FROM_SCOPE,
        EventSolutionReason.SUPPLIES_WERE_GIVEN,
        EventSolutionReason.OTHER,
    },
    EventType.NETWORK_ACCESS_ISSUES: {
        EventSolutionReason.PERMISSION_GRANTED,
        EventSolutionReason.AFFECTED_RESOURCE_REMOVED_FROM_SCOPE,
        EventSolutionReason.OTHER,
    },
    EventType.OTHER: {
        EventSolutionReason.OTHER,
    },
    EventType.REMOTE_ACCESS_ISSUES: {
        EventSolutionReason.ACCESS_GRANTED,
        EventSolutionReason.AFFECTED_RESOURCE_REMOVED_FROM_SCOPE,
        EventSolutionReason.OTHER,
    },
    EventType.TOE_DIFFERS_APPROVED: {
        EventSolutionReason.TOE_CHANGE_APPROVED,
        EventSolutionReason.TOE_WILL_REMAIN_UNCHANGED,
    },
    EventType.VPN_ISSUES: {
        EventSolutionReason.ACCESS_GRANTED,
        EventSolutionReason.AFFECTED_RESOURCE_REMOVED_FROM_SCOPE,
        EventSolutionReason.OTHER,
    },
}
