""" Implementation of custom exceptions for Integrates """
from typing import Sequence


class SecureAccessException(Exception):
    """ Exception that controls access to resources with authentication. """
    def __init__(self) -> None:
        """ Constructor """
        msg = "Exception - Access to resources without active session"
        super(SecureAccessException, self).__init__(msg)


class SecureParamsException(Exception):
    """ Exception to control parameter validation. """
    def __init__(self) -> None:
        """ Constructor """
        msg = "Exception - Incorrect or missing parameters"
        super(SecureParamsException, self).__init__(msg)


class APIConnectionException(Exception):
    """ Exception to control communication with the backend. """
    def __init__(self) -> None:
        """ Constructor """
        msg = "Excepcion - Error de conexion con el servidor"
        super(APIConnectionException, self).__init__(msg)


class LogicException(Exception):
    """ Exception to control general logical errors. """
    def __init__(self, code: int = 99) -> None:
        """ Constructor. """
        if code == 100:
            msg = "E100 - Username or Password is incorrect"
        elif code == 101:
            msg = "E101 - Other"
        else:
            msg = "E102 - Unexpected error"
        super(LogicException, self).__init__(msg)


class RequestedReportError(Exception):
    """ Exception to control pdf, xls or data report error. """
    def __init__(self) -> None:
        msg = "Error - Some error ocurred generating the report"
        super(RequestedReportError, self).__init__(msg)


class InvalidAcceptanceDays(Exception):
    """ Exception to control correct input in organization settings """
    def __init__(self, expr: str = '') -> None:
        if expr:
            msg = f'Exception - {expr}'
        else:
            msg = (
                'Exception - Acceptance days should be a positive integer'
            )
        super(InvalidAcceptanceDays, self).__init__(msg)


class InvalidAcceptanceSeverity(Exception):
    def __init__(self, expr: str = '') -> None:
        if expr:
            msg = (
                'Exception - Vulnerability cannot be accepted, severity '
                'outside of range set by the organization'
            )
        else:
            msg = (
                'Exception - Severity value should be a positive '
                'floating number between 0.0 a 10.0'
            )
        super(InvalidAcceptanceSeverity, self).__init__(msg)


class InvalidAcceptanceSeverityRange(Exception):
    def __init__(self) -> None:
        msg = (
            'Exception - Min acceptance severity value should not '
            'be higher than the max value'
        )
        super(InvalidAcceptanceSeverityRange, self).__init__(msg)


class InvalidNumberAcceptations(Exception):
    def __init__(self, expr: str = '') -> None:
        if expr:
            msg = (
                'Exception - Vulnerability has been accepted the maximum '
                'number of times allowed by the organization'
            )
        else:
            msg = (
                'Exception - Number of acceptations should be zero or positive'
            )
        super(InvalidNumberAcceptations, self).__init__(msg)


class InvalidVulnsNumber(Exception):
    """Exception to control number of vulnerabilities provided to upload."""
    def __init__(self) -> None:
        msg = (
            'Exception - You can upload a maximum of '
            '100 vulnerabilities per file'
        )
        super(InvalidVulnsNumber, self).__init__(msg)


class InvalidRange(Exception):
    """Exception to control valid range in vulnerabilities."""
    def __init__(self, expr: str = '') -> None:
        """ Constructor """
        msg = f'{{"msg": "Exception - Error in range limit numbers", {expr}}}'
        super(InvalidRange, self).__init__(msg)


class InvalidSchema(Exception):
    """Exception to control schema validation."""
    def __init__(self, expr: str = '') -> None:
        """ Constructor """
        msg = f'{{"msg": "Exception - Invalid Schema", {expr}}}'
        super(InvalidSchema, self).__init__(msg)


class InvalidStream(Exception):
    """Exception to control stream validation."""
    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Invalid Stream'
        super(InvalidStream, self).__init__(msg)


class InvalidFileSize(Exception):
    """Exception to control file size."""
    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Invalid File Size'
        super(InvalidFileSize, self).__init__(msg)


class InvalidFileStructure(Exception):
    """Exception to control file structure."""
    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Wrong File Structure'
        super(InvalidFileStructure, self).__init__(msg)


class InvalidExpirationTime(Exception):
    """Exception to control valid expiration time."""
    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Invalid Expiration Time'
        super(InvalidExpirationTime, self).__init__(msg)


class InvalidFileType(Exception):
    """Exception to control file type."""
    def __init__(self, detail: str = '') -> None:
        """ Constructor """
        msg = 'Exception - Invalid File Type'
        if detail:
            msg += f': {detail}'
        super(InvalidFileType, self).__init__(msg)


class ErrorUploadingFileS3(Exception):
    """Exception to control upload of files in s3."""
    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Error Uploading File to S3'
        super(ErrorUploadingFileS3, self).__init__(msg)


class InvalidAuthorization(Exception):
    """Exception to control authorization."""
    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Invalid Authorization'
        super(InvalidAuthorization, self).__init__(msg)


class InvalidPath(Exception):
    """Exception to control valid path value in vulnerabilities."""
    def __init__(self, expr: str) -> None:
        """ Constructor """
        msg = f'{{"msg": "Exception - Error in path value", {expr}}}'
        super(InvalidPath, self).__init__(msg)


class InvalidPort(Exception):
    """Exception to control valid port value in vulnerabilities."""
    def __init__(self, expr: str = '') -> None:
        """ Constructor """
        msg = f'{{"msg": "Exception - Error in port value", {expr}}}'
        super(InvalidPort, self).__init__(msg)


class InvalidParameter(Exception):
    """Exception to control empty parameter"""
    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Error empty value is not valid'
        super(InvalidParameter, self).__init__(msg)


class InvalidRootExclusion(Exception):
    """Exception to control exclusion paths"""
    def __init__(self) -> None:
        """ Constructor """
        msg = (
            'Exception - Root name should not be included in the exception '
            'pattern'
        )
        super(InvalidRootExclusion, self).__init__(msg)


class InvalidProjectName(Exception):
    """Exception to control invalid project name"""
    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Error invalid project name'
        super(InvalidProjectName, self).__init__(msg)


class InvalidProjectServicesConfig(Exception):
    """Exception to control that services attached to a project are valid."""
    def __init__(self, msg: str) -> None:
        """ Constructor """
        super(InvalidProjectServicesConfig, self).__init__(
            f'Exception - {msg}')


class EmptyPoolName(Exception):
    """Exception to control an empty pool of groups name"""
    def __init__(self, entity: str) -> None:
        """ Constructor """
        msg = (
            f'Exception - There are no {entity} names available at the moment'
        )
        super(EmptyPoolName, self).__init__(msg)


class InvalidSpecific(Exception):
    """Exception to control valid specific value in vulnerabilities."""
    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Error in specific value'
        super(InvalidSpecific, self).__init__(msg)


class InvalidField(Exception):
    """Exception to control invalid fields in forms"""
    def __init__(self, field: str = 'field') -> None:
        """Constructor"""
        msg = f'Exception - Invalid {field} in form'
        super(InvalidField, self).__init__(msg)


class InvalidChar(Exception):
    """Exception to control invalid characters in forms"""

    def __init__(self) -> None:
        msg = f'Exception - Invalid characters'
        super(InvalidChar, self).__init__(msg)


class InvalidFieldLength(Exception):
    """Exception to control invalid field length in forms"""
    def __init__(self) -> None:
        """Constructor"""
        msg = 'Exception - Invalid field length in form'
        super(InvalidFieldLength, self).__init__(msg)


class InvalidProject(Exception):
    """Exception to control a valid project."""
    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Project does not exist'
        super(InvalidProject, self).__init__(msg)


class ConcurrentSession(Exception):
    """
    Exception to control if an user
    has another active session when logging
    """
    def __init__(self) -> None:
        msg = 'Exception - User had a previous active session'
        super(ConcurrentSession, self).__init__(msg)


class ExpiredToken(Exception):
    """Exception to control if an user token exists, so has not expired"""
    def __init__(self) -> None:
        msg = 'Exception - User token has expired'
        super(ExpiredToken, self).__init__(msg)


class QueryDepthExceeded(Exception):
    """Exception to control graphql max query depth"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Max query depth exceeded'
        super(QueryDepthExceeded, self).__init__(msg)


class FileInfected(Exception):
    """Exception if an uploaded file is infected"""

    def __init__(self) -> None:
        msg = 'Exception - File infected'
        super(FileInfected, self).__init__(msg)


class FindingNotFound(Exception):
    """Exception to control finding data availability"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Access denied'
        super(FindingNotFound, self).__init__(msg)


class InvalidDate(Exception):
    """Exception to control the date inserted in an Accepted finding"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - The inserted date is invalid'
        super(InvalidDate, self).__init__(msg)


class AlreadyApproved(Exception):
    """Exception to control draft-only operations"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - This draft has already been approved'
        super(AlreadyApproved, self).__init__(msg)


class DraftWithoutVulns(Exception):
    """Exception to control draft approvation process"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'CANT_APPROVE_FINDING_WITHOUT_VULNS'
        super(DraftWithoutVulns, self).__init__(msg)


class AlreadySubmitted(Exception):
    """Exception to control submitted drafts"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - This draft has already been submitted'
        super(AlreadySubmitted, self).__init__(msg)


class IncompleteDraft(Exception):
    """Exception to control draft submission"""

    def __init__(self, fields: Sequence[str]) -> None:
        """ Constructor """
        msg = f'Exception - This draft has missing fields: {", ".join(fields)}'
        super(IncompleteDraft, self).__init__(msg)


class InvalidDraftTitle(Exception):
    """Exception to control draft titles"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - The inserted title is invalid'
        super(InvalidDraftTitle, self).__init__(msg)


class InvalidDateFormat(Exception):
    """Exception to control the date format inserted in an Accepted finding"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - The date format is invalid'
        super(InvalidDateFormat, self).__init__(msg)


class NotSubmitted(Exception):
    """Exception to control unsubmitted drafts"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - The draft has not been submitted yet'
        super(NotSubmitted, self).__init__(msg)


class EventNotFound(Exception):
    """Exception to control event data availability"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Event not found'
        super(EventNotFound, self).__init__(msg)


class EventAlreadyClosed(Exception):
    """Exception to control event updates"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - The event has already been closed'
        super(EventAlreadyClosed, self).__init__(msg)


class UnexpectedUserRole(Exception):
    """Exception to control that roles attached to an user are valid."""

    def __init__(self, msg: str) -> None:
        """ Constructor """
        super(UnexpectedUserRole, self).__init__(f'Exception - {msg}')


class UserNotFound(Exception):
    """Exception to control user search"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - User not Found'
        super(UserNotFound, self).__init__(msg)


class UserNotInOrganization(Exception):
    """
    Exception to control user access to organizations
    """
    def __init__(self, expr: str = '') -> None:
        if expr:
            msg = 'Exception - User is not a member of the target organization'
        else:
            msg = 'Access denied'
        super(UserNotInOrganization, self).__init__(msg)


class GroupNotInOrganization(Exception):
    """
    Exception to control that a group belongs to an organization
    """
    def __init__(self) -> None:
        msg = 'Exception - Group does not belong to the organization specified'
        super(GroupNotInOrganization, self).__init__(msg)


class InvalidSeverity(Exception):
    """Exception to control severity value"""

    def __init__(self, fields: Sequence[int]) -> None:
        """ Constructor """
        msg = (
            'Exception - Severity value must be between '
            f'{fields[0]} and {fields[1]}'
        )
        super(InvalidSeverity, self).__init__(msg)


class SameValues(Exception):
    """Exception to control save values updating treatment"""

    def __init__(self) -> None:
        msg = 'Exception - Same values'
        super(SameValues, self).__init__(msg)


class PermissionDenied(Exception):
    """Exception to control permission"""

    def __init__(self) -> None:
        msg = 'Exception - Error permission denied'
        super(PermissionDenied, self).__init__(msg)


class AlreadyPendingDeletion(Exception):
    """Exception to control pending to delete projects"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - This project has already been deleted or is pending'
        super(AlreadyPendingDeletion, self).__init__(msg)


class NotPendingDeletion(Exception):
    """Exception to control not pending to delete projects"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - The project is not pending to delete'
        super(NotPendingDeletion, self).__init__(msg)


class AlreadyRequested(Exception):
    """Exception to control verification already requested"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Request verification already requested'
        super(AlreadyRequested, self).__init__(msg)


class NotVerificationRequested(Exception):
    """Exception to control finding verification"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Error verification not requested'
        super(NotVerificationRequested, self).__init__(msg)


class VulnNotInFinding(Exception):
    """
    Exception to control vulnerability in finding
    """
    def __init__(self) -> None:
        msg = 'Exception - Vulnerability does not belong to finding'
        super(VulnNotInFinding, self).__init__(msg)


class AlreadyZeroRiskRequested(Exception):
    """Exception to control zero risk already is already requested"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Zero risk vulnerability is already requested'
        super(AlreadyZeroRiskRequested, self).__init__(msg)


class NotZeroRiskRequested(Exception):
    """Exception to control zero risk already is not requested"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Zero risk vulnerability is not requested'
        super(NotZeroRiskRequested, self).__init__(msg)


class EvidenceNotFound(Exception):
    """Exception to control evidence data availability"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Evidence not found'
        super(EvidenceNotFound, self).__init__(msg)


class VulnAlreadyClosed(Exception):
    """Exception to control vulnerability updates"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - The vulnerability has already been closed'
        super(VulnAlreadyClosed, self).__init__(msg)


class VulnNotFound(Exception):
    """Exception to control vulnerability data availability"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Vulnerability not found'
        super(VulnNotFound, self).__init__(msg)


class RepeatedRoot(Exception):
    """Exception to prevent repeated roots"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Active root with the same URL/branch already exists'
        super(RepeatedRoot, self).__init__(msg)


class RepeatedValues(Exception):
    """Exception to prevent repeated values"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - One or more values already exist'
        super(RepeatedValues, self).__init__(msg)


class InvalidCommentParent(Exception):
    """Exception to prevent repeated values"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Comment parent is invalid'
        super(InvalidCommentParent, self).__init__(msg)


class InvalidOrganization(Exception):
    """Exception to prevent repeated organizations"""

    def __init__(self) -> None:
        """ Constructor """
        msg = f'Access denied'
        super(InvalidOrganization, self).__init__(msg)


class DocumentNotFound(Exception):
    """Exception to control analytics data availability"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Document not found'
        super(DocumentNotFound, self).__init__(msg)


class InvalidPushToken(Exception):
    """Exception to validate mobile push token format"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Invalid push token'
        super(InvalidPushToken, self).__init__(msg)


class UnavailabilityError(Exception):
    """Unavailability for some ClienErrors"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Service unavalible, please retry'
        super(UnavailabilityError, self).__init__(msg)


class OrganizationNotFound(Exception):
    """Exception to control organization availability"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Access denied or organization not found'
        super(OrganizationNotFound, self).__init__(msg)


class StakeholderNotFound(Exception):
    """Exception to control stakeholder availability"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Access denied or stakeholder not found'
        super(StakeholderNotFound, self).__init__(msg)


class GroupNotFound(Exception):
    """Exception to control group availability"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Access denied or group not found'
        super(GroupNotFound, self).__init__(msg)


class TagNotFound(Exception):
    """Exception to control tag availability"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Access denied or tag not found'
        super(TagNotFound, self).__init__(msg)


class InvalidJustificationMaxLength(Exception):
    """Exception to control justification length"""

    def __init__(self, field: int) -> None:
        """ Constructor """
        msg = (
            'Exception - Justification must have a maximum of '
            f'{field} characters'
        )
        super(InvalidJustificationMaxLength, self).__init__(msg)


class InvalidTreatmentManager(Exception):
    """Exception to control if treatment manager is valid"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Invalid treatment manager'
        super(InvalidTreatmentManager, self).__init__(msg)


class AcceptionNotRequested(Exception):
    """Exception to control if acceptation is not valid"""

    def __init__(self) -> None:
        """ Constructor """
        msg = (
            'Exception - It cant handle acceptation without being requested'
        )
        super(AcceptionNotRequested, self).__init__(msg)


class RootNotFound(Exception):
    def __init__(self) -> None:
        msg = 'Exception - Access denied or root not found'
        super(RootNotFound, self).__init__(msg)


class StakeholderHasGroupAccess(Exception):
    def __init__(self) -> None:
        msg = (
            'Exception - The stakeholder has been granted access to '
            'the group previously'
        )
        super(StakeholderHasGroupAccess, self).__init__(msg)


class InvalidSource(Exception):
    """Exception to control if the source is valid."""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Invalid source'
        super(InvalidSource, self).__init__(msg)
