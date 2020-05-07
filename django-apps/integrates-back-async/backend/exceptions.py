""" Implementation of custom exceptions for FluidIntegrates. """


class SecureAccessException(Exception):
    """ Exception that controls access to resources with authentication. """
    def __init__(self):
        """ Constructor """
        msg = "Exception - Access to resources without active session"
        super(SecureAccessException, self).__init__(msg)


class SecureParamsException(Exception):
    """ Exception to control parameter validation. """
    def __init__(self):
        """ Constructor """
        msg = "Exception - Incorrect or missing parameters"
        super(SecureParamsException, self).__init__(msg)


class APIConnectionException(Exception):
    """ Exception to control communication with the backend. """
    def __init__(self):
        """ Constructor """
        msg = "Excepcion - Error de conexion con el servidor"
        super(APIConnectionException, self).__init__(msg)


class LogicException(Exception):
    """ Exception to control general logical errors. """
    def __init__(self, code=99):
        """ Constructor. """
        if code == 100:
            msg = "E100 - Username or Password is incorrect"
        elif code == 101:
            msg = "E101 - Other"
        else:
            msg = "E102 - Unexpected error"
        super(LogicException, self).__init__(msg)


class InvalidRange(Exception):
    """Exception to control valid range in vulnerabilities."""
    def __init__(self, expr=''):
        """ Constructor """
        msg = f'{{"msg": "Exception - Error in range limit numbers", {expr}}}'
        super(InvalidRange, self).__init__(msg)


class InvalidSchema(Exception):
    """Exception to control schema validation."""
    def __init__(self, expr=''):
        """ Constructor """
        msg = '{{"msg": "Exception - Invalid Schema", {expr}}}'.format(
            expr=expr
        )
        super(InvalidSchema, self).__init__(msg)


class InvalidFileSize(Exception):
    """Exception to control file size."""
    def __init__(self):
        """ Constructor """
        msg = 'Exception - Invalid File Size'
        super(InvalidFileSize, self).__init__(msg)


class InvalidFileStructure(Exception):
    """Exception to control file structure."""
    def __init__(self):
        """ Constructor """
        msg = 'Exception - Wrong File Structure'
        super(InvalidFileStructure, self).__init__(msg)


class InvalidExpirationTime(Exception):
    """Exception to control valid expiration time."""
    def __init__(self):
        """ Constructor """
        msg = 'Exception - Invalid Expiration Time'
        super(InvalidExpirationTime, self).__init__(msg)


class InvalidFileType(Exception):
    """Exception to control file type."""
    def __init__(self, detail=''):
        """ Constructor """
        msg = 'Exception - Invalid File Type'
        if detail:
            msg += f': {detail}'
        super(InvalidFileType, self).__init__(msg)


class ErrorUploadingFileS3(Exception):
    """Exception to control upload of files in s3."""
    def __init__(self):
        """ Constructor """
        msg = 'Exception - Error Uploading File to S3'
        super(ErrorUploadingFileS3, self).__init__(msg)


class InvalidAuthorization(Exception):
    """Exception to control authorization."""
    def __init__(self):
        """ Constructor """
        msg = 'Exception - Invalid Authorization'
        super(InvalidAuthorization, self).__init__(msg)


class InvalidPath(Exception):
    """Exception to control valid path value in vulnerabilities."""
    def __init__(self, expr):
        """ Constructor """
        msg = '{{"msg": "Exception - Error in path value", {expr}}}'.format(
            expr=expr
        )
        super(InvalidPath, self).__init__(msg)


class InvalidPort(Exception):
    """Exception to control valid port value in vulnerabilities."""
    def __init__(self, expr=''):
        """ Constructor """
        msg = '{{"msg": "Exception - Error in port value", {expr}}}'.format(
            expr=expr
        )
        super(InvalidPort, self).__init__(msg)


class InvalidParameter(Exception):
    """Exception to control empty parameter"""
    def __init__(self):
        """ Constructor """
        msg = 'Exception - Error empty value is not valid'
        super(InvalidParameter, self).__init__(msg)


class InvalidProjectName(Exception):
    """Exception to control invalid project name"""
    def __init__(self):
        """ Constructor """
        msg = 'Exception - Error invalid project name'
        super(InvalidProjectName, self).__init__(msg)


class InvalidProjectServicesConfig(Exception):
    """Exception to control that services attached to a project are valid."""
    def __init__(self, msg):
        """ Constructor """
        super(InvalidProjectServicesConfig, self).__init__(
            f'Exception - {msg}')


class EmptyPoolProjectName(Exception):
    """Exception to control an empty pool of project name"""
    def __init__(self):
        """ Constructor """
        msg = 'Exception - Currently you cannot create projects'
        super(EmptyPoolProjectName, self).__init__(msg)


class InvalidSpecific(Exception):
    """Exception to control valid specific value in vulnerabilities."""
    def __init__(self):
        """ Constructor """
        msg = 'Exception - Error in specific value'
        super(InvalidSpecific, self).__init__(msg)


class InvalidField(Exception):
    """Exception to control invalid fields in forms"""
    def __init__(self, field='field'):
        """Constructor"""
        msg = 'Exception - Invalid {} in form'.format(field)
        super(InvalidField, self).__init__(msg)


class InvalidProject(Exception):
    """Exception to control a valid project."""
    def __init__(self):
        """ Constructor """
        msg = 'Exception - Project does not exist'
        super(InvalidProject, self).__init__(msg)


class QueryDepthExceeded(Exception):
    """Exception to control graphql max query depth"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - Max query depth exceeded'
        super(QueryDepthExceeded, self).__init__(msg)


class FindingNotFound(Exception):
    """Exception to control finding data availability"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - Finding not found'
        super(FindingNotFound, self).__init__(msg)


class InvalidDate(Exception):
    """Exception to control the date inserted in an Accepted finding"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - The inserted date is invalid'
        super(InvalidDate, self).__init__(msg)


class AlreadyApproved(Exception):
    """Exception to control draft-only operations"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - This draft has already been approved'
        super(AlreadyApproved, self).__init__(msg)


class AlreadySubmitted(Exception):
    """Exception to control submitted drafts"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - This draft has already been submitted'
        super(AlreadySubmitted, self).__init__(msg)


class IncompleteDraft(Exception):
    """Exception to control draft submission"""

    def __init__(self, fields):
        """ Constructor """
        msg = 'Exception - This draft has missing fields: {}'.format(
            ', '.join(fields))
        super(IncompleteDraft, self).__init__(msg)


class InvalidDraftTitle(Exception):
    """Exception to control draft titles"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - The inserted title is invalid'
        super(InvalidDraftTitle, self).__init__(msg)


class InvalidDateFormat(Exception):
    """Exception to control the date format inserted in an Accepted finding"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - The date format is invalid'
        super(InvalidDateFormat, self).__init__(msg)


class NotSubmitted(Exception):
    """Exception to control unsubmitted drafts"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - The draft has not been submitted yet'
        super(NotSubmitted, self).__init__(msg)


class EventNotFound(Exception):
    """Exception to control event data availability"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - Event not found'
        super(EventNotFound, self).__init__(msg)


class EventAlreadyClosed(Exception):
    """Exception to control event updates"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - The event has already been closed'
        super(EventAlreadyClosed, self).__init__(msg)


class UserNotFound(Exception):
    """Exception to control user search"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - User not Found'
        super(UserNotFound, self).__init__(msg)


class InvalidSeverity(Exception):
    """Exception to control severity value"""

    def __init__(self, fields):
        """ Constructor """
        msg = f'Exception - Severity value must be between {fields[0]} and {fields[1]}'
        super(InvalidSeverity, self).__init__(msg)


class SameValues(Exception):
    """Exception to control save values updating treatment"""

    def __init__(self):
        msg = 'Exception - Same values'
        super(SameValues, self).__init__(msg)


class PermissionDenied(Exception):
    """Exception to control permission"""

    def __init__(self):
        msg = 'Exception - Error permission denied'
        super(PermissionDenied, self).__init__(msg)


class AlreadyPendingDeletion(Exception):
    """Exception to control pending to delete projects"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - This project has already been deleted or is pending'
        super(AlreadyPendingDeletion, self).__init__(msg)


class NotPendingDeletion(Exception):
    """Exception to control not pending to delete projects"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - The project is not pending to delete'
        super(NotPendingDeletion, self).__init__(msg)


class AlreadyRequested(Exception):
    """Exception to control verification already requested"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - Request verification already requested'
        super(AlreadyRequested, self).__init__(msg)


class NotVerificationRequested(Exception):
    """Exception to control finding verification"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - Error verification not requested'
        super(NotVerificationRequested, self).__init__(msg)


class EvidenceNotFound(Exception):
    """Exception to control evidence data availability"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - Evidence not found'
        super(EvidenceNotFound, self).__init__(msg)


class VulnAlreadyClosed(Exception):
    """Exception to control vulnerability updates"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - The vulnerability has already been closed'
        super(VulnAlreadyClosed, self).__init__(msg)


class VulnNotFound(Exception):
    """Exception to control vulnerability data availability"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - Vulnerability not found'
        super(VulnNotFound, self).__init__(msg)


class RepeatedValues(Exception):
    """Exception to prevent repeated values"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - One or more values already exist'
        super(RepeatedValues, self).__init__(msg)


class InvalidCommentParent(Exception):
    """Exception to prevent repeated values"""

    def __init__(self):
        """ Constructor """
        msg = 'Exception - Comment parent is invalid'
        super(InvalidCommentParent, self).__init__(msg)
