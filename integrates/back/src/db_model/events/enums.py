# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)


class EventEvidenceId(str, Enum):
    FILE_1: str = "FILE_1"
    IMAGE_1: str = "IMAGE_1"
    IMAGE_2: str = "IMAGE_2"
    IMAGE_3: str = "IMAGE_3"
    IMAGE_4: str = "IMAGE_4"
    IMAGE_5: str = "IMAGE_5"
    IMAGE_6: str = "IMAGE_6"


class EventStateStatus(str, Enum):
    CREATED: str = "CREATED"
    OPEN: str = "OPEN"
    SOLVED: str = "SOLVED"
    VERIFICATION_REQUESTED: str = "VERIFICATION_REQUESTED"


class EventSolutionReason(str, Enum):
    ACCESS_GRANTED: str = "ACCESS_GRANTED"
    AFFECTED_RESOURCE_REMOVED_FROM_SCOPE: str = (
        "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE"
    )
    CLONED_SUCCESSFULLY: str = "CLONED_SUCCESSFULLY"
    CREDENTIALS_ARE_WORKING_NOW: str = "CREDENTIALS_ARE_WORKING_NOW"
    DATA_UPDATED: str = "DATA_UPDATED"
    ENVIRONMENT_IS_WORKING_NOW: str = "ENVIRONMENT_IS_WORKING_NOW"
    INSTALLER_IS_WORKING_NOW: str = "INSTALLER_IS_WORKING_NOW"
    IS_OK_TO_RESUME: str = "IS_OK_TO_RESUME"
    NEW_CREDENTIALS_PROVIDED: str = "NEW_CREDENTIALS_PROVIDED"
    NEW_ENVIRONMENT_PROVIDED: str = "NEW_ENVIRONMENT_PROVIDED"
    OTHER: str = "OTHER"
    PERMISSION_DENIED: str = "PERMISSION_DENIED"
    PERMISSION_GRANTED: str = "PERMISSION_GRANTED"
    # Reason will be removed
    PROBLEM_SOLVED: str = "PROBLEM_SOLVED"
    SUPPLIES_WERE_GIVEN: str = "SUPPLIES_WERE_GIVEN"
    TOE_CHANGE_APPROVED: str = "TOE_CHANGE_APPROVED"
    TOE_WILL_REMAIN_UNCHANGED: str = "TOE_WILL_REMAIN_UNCHANGED"


class EventType(str, Enum):
    AUTHORIZATION_SPECIAL_ATTACK: str = "AUTHORIZATION_SPECIAL_ATTACK"
    CLIENT_CANCELS_PROJECT_MILESTONE: str = "CLIENT_CANCELS_PROJECT_MILESTONE"
    CLIENT_EXPLICITLY_SUSPENDS_PROJECT: str = (
        "CLIENT_EXPLICITLY_SUSPENDS_PROJECT"
    )
    CLONING_ISSUES: str = "CLONING_ISSUES"
    CREDENTIAL_ISSUES: str = "CREDENTIAL_ISSUES"
    DATA_UPDATE_REQUIRED: str = "DATA_UPDATE_REQUIRED"
    ENVIRONMENT_ISSUES: str = "ENVIRONMENT_ISSUES"
    INSTALLER_ISSUES: str = "INSTALLER_ISSUES"
    # It will be replaced
    INCORRECT_MISSING_SUPPLIES: str = "INCORRECT_MISSING_SUPPLIES"
    MISSING_SUPPLIES: str = "MISSING_SUPPLIES"
    NETWORK_ACCESS_ISSUES: str = "NETWORK_ACCESS_ISSUES"
    OTHER: str = "OTHER"
    REMOTE_ACCESS_ISSUES: str = "REMOTE_ACCESS_ISSUES"
    TOE_DIFFERS_APPROVED: str = "TOE_DIFFERS_APPROVED"
    VPN_ISSUES: str = "VPN_ISSUES"
