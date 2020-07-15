""" Implementation of custom exceptions for FluidIntegrates. """
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
                'Exception - Acceptance days should be a positive integer '
                'between 0 and 180'
            )
        super(InvalidAcceptanceDays, self).__init__(msg)


class InvalidAcceptanceSeverity(Exception):
    def __init__(self, expr: str = '') -> None:
        if expr:
            msg = (
                'Exception - Finding cannot be accepted, severity outside of '
                'range set by the organization'
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
                'Exception - Finding has been accepted the maximum number of '
                'times allowed by the organization'
            )
        else:
            msg = (
                'Exception - Number of acceptations should be zero or positive'
            )
        super(InvalidNumberAcceptations, self).__init__(msg)


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


class EmptyPoolGroupName(Exception):
    """Exception to control an empty pool of groups name"""
    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - There are no group names available at the moment'
        super(EmptyPoolGroupName, self).__init__(msg)


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
        msg = 'Exception - Finding not found'
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
        msg = 'Exception - Organization name is invalid'
        super(InvalidOrganization, self).__init__(msg)


class InvalidResource(Exception):
    """Exception to inform that the resource does not exist"""

    def __init__(self) -> None:
        """ Constructor """
        msg = 'Exception - Resource does not exist'
        super(InvalidResource, self).__init__(msg)
