# pylint: disable=super-with-arguments
from __future__ import (
    annotations,
)

from typing import (
    Sequence,
)


class CustomBaseException(Exception):
    pass


class _SingleMessageException(CustomBaseException):
    msg: str

    @classmethod
    def new(cls) -> _SingleMessageException:
        return cls(cls.msg)


class ErrorUploadingFileS3(_SingleMessageException):
    msg: str = "Unable to upload file to S3 service"


class ExpectedEscaperField(_SingleMessageException):
    msg: str = "Expected escaper field for vuln with source 'escape'"


class ExpectedPathToStartWithRepo(_SingleMessageException):
    msg: str = "Expected path to start with the repo nickname"


class ExpectedVulnToBeOfLinesType(_SingleMessageException):
    msg: str = "Expected vulnerability to be of type: lines"


class ExpectedVulnToHaveNickname(_SingleMessageException):
    msg: str = "Expected vulnerability to have repo_nickname"


class InvalidCannotModifyNicknameWhenClosing(_SingleMessageException):
    msg: str = "Invalid, you cannot change the nickname while closing"


class InvalidNewVulnState(_SingleMessageException):
    msg: str = "Invalid, only New vulnerabilities with Open state are allowed"


class InvalidVulnerabilityAlreadyExists(_SingleMessageException):
    msg: str = "Invalid, vulnerability already exists"


class InvalidVulnCommitHash(_SingleMessageException):
    msg: str = "Commit Hash should be a 40 chars long hexadecimal"


class InvalidVulnSpecific(_SingleMessageException):
    msg: str = "Vulnerability Specific must be integer"


class InvalidVulnWhere(_SingleMessageException):
    msg: str = "Vulnerability where should match: ^(?!=)+[^/]+/.+$"


class SnapshotNotFound(_SingleMessageException):
    msg: str = "Snapshot not found in analytics bucket"


class UnableToSkimsQueue(_SingleMessageException):
    msg: str = "Unable to queue a verification request"


class UnableToSendMail(_SingleMessageException):
    msg: str = "Unable to send mail message"


class UnavailabilityError(_SingleMessageException):
    msg: str = "AWS service unavailable, please retry"


class AcceptanceNotRequested(CustomBaseException):
    """Exception to control if acceptance is not valid"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - It cant handle acceptance without being requested"
        super(AcceptanceNotRequested, self).__init__(msg)


class AlreadyApproved(CustomBaseException):
    """Exception to control draft-only operations"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - This draft has already been approved"
        super(AlreadyApproved, self).__init__(msg)


class AlreadyCreated(CustomBaseException):
    """Exception to control draft-only operations"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - This draft has already been created"
        super(AlreadyCreated, self).__init__(msg)


class AlreadyPendingDeletion(CustomBaseException):
    """Exception to control pending to delete groups"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - This group has already been deleted or is pending"
        super(AlreadyPendingDeletion, self).__init__(msg)


class AlreadyRequested(CustomBaseException):
    """Exception to control verification already requested"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Request verification already requested"
        super(AlreadyRequested, self).__init__(msg)


class AlreadySubmitted(CustomBaseException):
    """Exception to control submitted drafts"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - This draft has already been submitted"
        super(AlreadySubmitted, self).__init__(msg)


class AlreadyZeroRiskRequested(CustomBaseException):
    """Exception to control zero risk already is already requested"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Zero risk vulnerability is already requested"
        super(AlreadyZeroRiskRequested, self).__init__(msg)


class DocumentNotFound(CustomBaseException):
    """Exception to control analytics data availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Document not found"
        super(DocumentNotFound, self).__init__(msg)


class DraftWithoutVulns(CustomBaseException):
    """Exception to control draft approvation process"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "CANT_APPROVE_FINDING_WITHOUT_VULNS"
        super(DraftWithoutVulns, self).__init__(msg)


class EmptyPoolName(CustomBaseException):
    """Exception to control an empty pool of groups name"""

    def __init__(self, entity: str) -> None:
        """Constructor"""
        msg = (
            f"Exception - There are no {entity} names available at the moment"
        )
        super(EmptyPoolName, self).__init__(msg)


class EventAlreadyClosed(CustomBaseException):
    """Exception to control event updates"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The event has already been closed"
        super(EventAlreadyClosed, self).__init__(msg)


class EventNotFound(CustomBaseException):
    """Exception to control event data availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Event not found"
        super(EventNotFound, self).__init__(msg)


class EvidenceNotFound(CustomBaseException):
    """Exception to control evidence data availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Evidence not found"
        super(EvidenceNotFound, self).__init__(msg)


class ExpiredToken(CustomBaseException):
    """Exception to control if an user token exists, so has not expired"""

    def __init__(self) -> None:
        msg = "Exception - User token has expired"
        super(ExpiredToken, self).__init__(msg)


class FileInfected(CustomBaseException):
    """Exception if an uploaded file is infected"""

    def __init__(self) -> None:
        msg = "Exception - File infected"
        super(FileInfected, self).__init__(msg)


class FindingNotFound(CustomBaseException):
    """Exception to control finding data availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Access denied"
        super(FindingNotFound, self).__init__(msg)


class GroupNameNotFound(CustomBaseException):
    """Exception to control if the group name has been found."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Group name has not been found"
        super(GroupNameNotFound, self).__init__(msg)


class GroupNotFound(CustomBaseException):
    """Exception to control group availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Access denied or group not found"
        super(GroupNotFound, self).__init__(msg)


class HasOpenVulns(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - A root with open vulns can't be deactivated"
        super(HasOpenVulns, self).__init__(msg)


class IncompleteDraft(CustomBaseException):
    """Exception to control draft submission"""

    def __init__(self, fields: Sequence[str]) -> None:
        """Constructor"""
        msg = f'Exception - This draft has missing fields: {", ".join(fields)}'
        super(IncompleteDraft, self).__init__(msg)


class IncompleteSeverity(CustomBaseException):
    """Exception to control severity fields"""

    def __init__(self, fields: Sequence[str]) -> None:
        """Constructor"""
        msg = f'Exception - Severity has missing fields: {", ".join(fields)}'
        super(IncompleteSeverity, self).__init__(msg)


class InvalidAcceptanceDays(CustomBaseException):
    """Exception to control correct input in organization settings"""

    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = f"Exception - {expr}"
        else:
            msg = "Exception - Acceptance days should be a positive integer"
        super(InvalidAcceptanceDays, self).__init__(msg)


class InvalidAcceptanceSeverity(CustomBaseException):
    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = (
                "Exception - Vulnerability cannot be accepted, severity "
                "outside of range set by the organization"
            )
        else:
            msg = (
                "Exception - Severity value should be a positive "
                "floating number between 0.0 a 10.0"
            )
        super(InvalidAcceptanceSeverity, self).__init__(msg)


class InvalidAcceptanceSeverityRange(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - Min acceptance severity value should not "
            "be higher than the max value"
        )
        super(InvalidAcceptanceSeverityRange, self).__init__(msg)


class InvalidAuthorization(CustomBaseException):
    """Exception to control authorization."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid Authorization"
        super(InvalidAuthorization, self).__init__(msg)


class InvalidChar(CustomBaseException):
    """Exception to control invalid characters in forms"""

    def __init__(self) -> None:
        msg = "Exception - Invalid characters"
        super(InvalidChar, self).__init__(msg)


class InvalidFilter(CustomBaseException):
    """Exception to control the supported filters"""

    def __init__(self, filter_name: str) -> None:
        msg = f"Exception - The filter is not supported: {filter_name}"
        super(InvalidFilter, self).__init__(msg)


class InvalidCommentParent(CustomBaseException):
    """Exception to prevent repeated values"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Comment parent is invalid"
        super(InvalidCommentParent, self).__init__(msg)


class InvalidCvssField(CustomBaseException):
    """Exception to control cvss field values"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Cvss field value must be a number"
        super(InvalidCvssField, self).__init__(msg)


class InvalidCvssVersion(CustomBaseException):
    """Exception to control cvss version"""

    def __init__(self) -> None:
        """Constructor"""
        msg: str = "Invalid, cvss version is not supported"
        super(InvalidCvssVersion, self).__init__(msg)


class InvalidDate(CustomBaseException):
    """Exception to control the date inserted in an Accepted finding"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The inserted date is invalid"
        super(InvalidDate, self).__init__(msg)


class InvalidDateFormat(CustomBaseException):
    """Exception to control the date format inserted in an Accepted finding"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The date format is invalid"
        super(InvalidDateFormat, self).__init__(msg)


class InvalidDraftTitle(CustomBaseException):
    """Exception to control draft titles"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The inserted title is invalid"
        super(InvalidDraftTitle, self).__init__(msg)


class InvalidExpirationTime(CustomBaseException):
    """Exception to control valid expiration time."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid Expiration Time"
        super(InvalidExpirationTime, self).__init__(msg)


class InvalidField(CustomBaseException):
    """Exception to control invalid fields in forms"""

    def __init__(self, field: str = "field") -> None:
        """Constructor"""
        msg = f"Exception - Invalid {field} in form"
        super(InvalidField, self).__init__(msg)


class InvalidFieldLength(CustomBaseException):
    """Exception to control invalid field length in forms"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid field length in form"
        super(InvalidFieldLength, self).__init__(msg)


class InvalidFileSize(CustomBaseException):
    """Exception to control file size."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid File Size"
        super(InvalidFileSize, self).__init__(msg)


class InvalidFileStructure(CustomBaseException):
    """Exception to control file structure."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Wrong File Structure"
        super(InvalidFileStructure, self).__init__(msg)


class InvalidFileType(CustomBaseException):
    """Exception to control file type."""

    def __init__(self, detail: str = "") -> None:
        """Constructor"""
        msg = "Exception - Invalid File Type"
        if detail:
            msg += f": {detail}"
        super(InvalidFileType, self).__init__(msg)


class InvalidGroupName(CustomBaseException):
    """Exception to control invalid group name"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Error invalid group name"
        super(InvalidGroupName, self).__init__(msg)


class InvalidGroupServicesConfig(CustomBaseException):
    """Exception to control that services attached to a group are valid."""

    def __init__(self, msg: str) -> None:
        """Constructor"""
        super(InvalidGroupServicesConfig, self).__init__(f"Exception - {msg}")


class InvalidJustificationMaxLength(CustomBaseException):
    """Exception to control justification length"""

    def __init__(self, field: int) -> None:
        """Constructor"""
        msg = (
            "Exception - Justification must have a maximum of "
            f"{field} characters"
        )
        super(InvalidJustificationMaxLength, self).__init__(msg)


class InvalidNumberAcceptances(CustomBaseException):
    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = (
                "Exception - Vulnerability has been accepted the maximum "
                "number of times allowed by the organization"
            )
        else:
            msg = (
                "Exception - Number of acceptances should be zero or positive"
            )
        super(InvalidNumberAcceptances, self).__init__(msg)


class InvalidOrganization(CustomBaseException):
    """Exception to prevent repeated organizations"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Access denied"
        super(InvalidOrganization, self).__init__(msg)


class InvalidParameter(CustomBaseException):
    """Exception to control empty parameter"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Error empty value is not valid"
        super(InvalidParameter, self).__init__(msg)


class InvalidPath(CustomBaseException):
    """Exception to control valid path value in vulnerabilities."""

    def __init__(self, expr: str) -> None:
        """Constructor"""
        msg = f'{{"msg": "Exception - Error in path value", {expr}}}'
        super(InvalidPath, self).__init__(msg)


class InvalidPort(CustomBaseException):
    """Exception to control valid port value in vulnerabilities."""

    def __init__(self, expr: str = "") -> None:
        """Constructor"""
        msg = f'{{"msg": "Exception - Error in port value", {expr}}}'
        super(InvalidPort, self).__init__(msg)


class InvalidPushToken(CustomBaseException):
    """Exception to validate mobile push token format"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid push token"
        super(InvalidPushToken, self).__init__(msg)


class InvalidRange(CustomBaseException):
    """Exception to control valid range in vulnerabilities."""

    def __init__(self, expr: str = "") -> None:
        """Constructor"""
        msg = f'{{"msg": "Exception - Error in range limit numbers", {expr}}}'
        super(InvalidRange, self).__init__(msg)


class InvalidRoleProvided(CustomBaseException):
    """Exception to control that users only grant roles they're allowed to."""

    def __init__(self, role: str) -> None:
        """Constructor"""
        msg = f"Invalid role or not enough permissions to grant role: {role}"
        super(InvalidRoleProvided, self).__init__(f"Exception - {msg}")


class InvalidRootExclusion(CustomBaseException):
    """Exception to control exclusion paths"""

    def __init__(self) -> None:
        """Constructor"""
        msg = (
            "Exception - Root name should not be included in the exception "
            "pattern"
        )
        super(InvalidRootExclusion, self).__init__(msg)


class InvalidSchema(CustomBaseException):
    """Exception to control schema validation."""

    def __init__(self, expr: str = "") -> None:
        """Constructor"""
        msg = f'{{"msg": "Exception - Invalid Schema", {expr}}}'
        super(InvalidSchema, self).__init__(msg)


class InvalidSeverity(CustomBaseException):
    """Exception to control severity value"""

    def __init__(self, fields: Sequence[int]) -> None:
        """Constructor"""
        msg = (
            "Exception - Severity value must be between "
            f"{fields[0]} and {fields[1]}"
        )
        super(InvalidSeverity, self).__init__(msg)


class InvalidSource(CustomBaseException):
    """Exception to control if the source is valid."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid source"
        super(InvalidSource, self).__init__(msg)


class InvalidSpecific(CustomBaseException):
    """Exception to control valid specific value in vulnerabilities."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Error in specific value"
        super(InvalidSpecific, self).__init__(msg)


class InvalidStream(CustomBaseException):
    """Exception to control stream validation."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid Stream"
        super(InvalidStream, self).__init__(msg)


class InvalidStateStatus(CustomBaseException):
    """Exception to control state status."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Invalid state status"
        super(InvalidStateStatus, self).__init__(msg)


class InvalidTreatmentManager(CustomBaseException):
    """Exception to control if treatment manager is valid"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Invalid treatment manager"
        super(InvalidTreatmentManager, self).__init__(msg)


class InvalidUserProvided(CustomBaseException):
    """Exception to control that users belong to Fluid Attacks before they're
    granted a restricted role"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "This role can only be granted to Fluid Attacks users"
        super(InvalidUserProvided, self).__init__(f"Exception - {msg}")


class InvalidVulnsNumber(CustomBaseException):
    """Exception to control number of vulnerabilities provided to upload."""

    def __init__(self) -> None:
        msg = (
            "Exception - You can upload a maximum of "
            "100 vulnerabilities per file"
        )
        super(InvalidVulnsNumber, self).__init__(msg)


class NotVerificationRequested(CustomBaseException):
    """Exception to control finding verification"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Error verification not requested"
        super(NotVerificationRequested, self).__init__(msg)


class NotSubmitted(CustomBaseException):
    """Exception to control unsubmitted drafts"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The draft has not been submitted yet"
        super(NotSubmitted, self).__init__(msg)


class NotZeroRiskRequested(CustomBaseException):
    """Exception to control zero risk already is not requested"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Zero risk vulnerability is not requested"
        super(NotZeroRiskRequested, self).__init__(msg)


class NotCvssVersion(CustomBaseException):
    """Exception to control cvss version is required"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - CvssVersion is required"
        super(NotCvssVersion, self).__init__(msg)


class OrganizationNotFound(CustomBaseException):
    """Exception to control organization availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Access denied or organization not found"
        super(OrganizationNotFound, self).__init__(msg)


class PermissionDenied(CustomBaseException):
    """Exception to control permission"""

    def __init__(self) -> None:
        msg = "Exception - Error permission denied"
        super(PermissionDenied, self).__init__(msg)


class RepeatedRoot(CustomBaseException):
    """Exception to prevent repeated roots"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Active root with the same URL/branch already exists"
        super(RepeatedRoot, self).__init__(msg)


class RepeatedRootNickname(CustomBaseException):
    """Exception to prevent repeated roots"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Active root with the same Nickname already exists"
        super(RepeatedRootNickname, self).__init__(msg)


class RepeatedToeInput(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Toe input already exists"
        super(RepeatedToeInput, self).__init__(msg)


class RepeatedToeLines(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Toe lines already exists"
        super(RepeatedToeLines, self).__init__(msg)


class RepeatedValues(CustomBaseException):
    """Exception to prevent repeated values"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - One or more values already exist"
        super(RepeatedValues, self).__init__(msg)


class RequestedReportError(CustomBaseException):
    """Exception to control pdf, xls or data report error."""

    def __init__(self) -> None:
        msg = "Error - Some error ocurred generating the report"
        super(RequestedReportError, self).__init__(msg)


class RootNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Access denied or root not found"
        super(RootNotFound, self).__init__(msg)


class SameValues(CustomBaseException):
    """Exception to control save values updating treatment"""

    def __init__(self) -> None:
        msg = "Exception - Same values"
        super(SameValues, self).__init__(msg)


class SecureAccessException(CustomBaseException):
    """Exception that controls access to resources with authentication."""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Access to resources without active session"
        super(SecureAccessException, self).__init__(msg)


class StakeholderHasGroupAccess(CustomBaseException):
    def __init__(self) -> None:
        msg = (
            "Exception - The stakeholder has been granted access to "
            "the group previously"
        )
        super(StakeholderHasGroupAccess, self).__init__(msg)


class StakeholderNotFound(CustomBaseException):
    """Exception to control stakeholder availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Access denied or stakeholder not found"
        super(StakeholderNotFound, self).__init__(msg)


class TagNotFound(CustomBaseException):
    """Exception to control tag availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Access denied or tag not found"
        super(TagNotFound, self).__init__(msg)


class ToeInputNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Toe input has not been found"
        super(ToeInputNotFound, self).__init__(msg)


class ToeLinesNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Toe lines has not been found"
        super(ToeLinesNotFound, self).__init__(msg)


class UnexpectedUserRole(CustomBaseException):
    """Exception to control that roles attached to an user are valid."""

    def __init__(self, msg: str) -> None:
        """Constructor"""
        super(UnexpectedUserRole, self).__init__(f"Exception - {msg}")


class UserNotInOrganization(CustomBaseException):
    """
    Exception to control user access to organizations
    """

    def __init__(self, expr: str = "") -> None:
        if expr:
            msg = "Exception - User is not a member of the target organization"
        else:
            msg = "Access denied"
        super(UserNotInOrganization, self).__init__(msg)


class VulnAlreadyClosed(CustomBaseException):
    """Exception to control vulnerability updates"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - The vulnerability has already been closed"
        super(VulnAlreadyClosed, self).__init__(msg)


class VulnNotFound(CustomBaseException):
    """Exception to control vulnerability data availability"""

    def __init__(self) -> None:
        """Constructor"""
        msg = "Exception - Vulnerability not found"
        super(VulnNotFound, self).__init__(msg)


class VulnNotInFinding(CustomBaseException):
    """
    Exception to control vulnerability in finding
    """

    def __init__(self) -> None:
        msg = "Exception - Vulnerability does not belong to finding"
        super(VulnNotInFinding, self).__init__(msg)


class InvalidFindingNamePolicy(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The finding name is invalid"
        super(InvalidFindingNamePolicy, self).__init__(msg)


class RepeatedFindingNamePolicy(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - The finding name policy already exists"
        super(RepeatedFindingNamePolicy, self).__init__(msg)


class FindingNamePolicyNotFound(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - Finding name policy not found"
        super(FindingNamePolicyNotFound, self).__init__(msg)


class PolicyAlreadyHandled(CustomBaseException):
    def __init__(self) -> None:
        msg = "Exception - This policy has already been reviewed"
        super(PolicyAlreadyHandled, self).__init__(msg)
