# pylint: disable=import-error

from ariadne import ObjectType, EnumType

ALERT = ObjectType('Alert')
EVENT = ObjectType('Event')
FINDING = ObjectType('Finding')
FORCES_EXECUTIONS = ObjectType('ForcesExecutions')
INTERNAL_PROJECT_NAME = ObjectType('InternalProject')
ME = ObjectType('Me')
PROJECT = ObjectType('Project')
RESOURCE = ObjectType('Resource')
USER = ObjectType('User')

DELETE_VULNERABILITY_JUSTIFICATION = EnumType(
    'DeleteVulnerabilityJustification',
    {
        'DUPLICATED': 'DUPLICATED',
        'FALSE_POSITIVE': 'FALSE_POSITIVE',
        'REPORTING_ERROR': 'REPORTING_ERROR',
    }
)
EVIDENCE_TYPE = EnumType(
    'EvidenceType',
    {
        'ANIMATION': 'animation',
        'EVIDENCE1': 'evidence_route_1',
        'EVIDENCE2': 'evidence_route_2',
        'EVIDENCE3': 'evidence_route_3',
        'EVIDENCE4': 'evidence_route_4',
        'EVIDENCE5': 'evidence_route_5',
        'EXPLOIT': 'exploit',
        'EXPLOITATION': 'exploitation',
        'RECORDS': 'fileRecords'
    }
)
EVIDENCE_DESCRIPTION_TYPE = EnumType(
    'EvidenceDescriptionType',
    {
        'EVIDENCE1': 'evidence_route_1',
        'EVIDENCE2': 'evidence_route_2',
        'EVIDENCE3': 'evidence_route_3',
        'EVIDENCE4': 'evidence_route_4',
        'EVIDENCE5': 'evidence_route_5'
    }
)
SUBSCRIPTION_TYPE = EnumType(
    'SubscriptionType',
    {
        'CONTINUOUS': 'continuous',
        'ONESHOT': 'oneshot'
    }
)
UPDATE_CLIENT_DESCRIPTION_TREATMENT = EnumType(
    'UpdateClientDescriptionTreatment',
    {
        'ACCEPTED': 'ACCEPTED',
        'ACCEPTED_UNDEFINED': 'ACCEPTED_UNDEFINED',
        'IN_PROGRESS': 'IN PROGRESS',
    }
)
FINDING_TYPE = EnumType(
    'FindingType',
    {
        'HYGIENE': 'HYGIENE',
        'SECURITY': 'SECURITY'
    }
)
FINDING_COMMENT_TYPE = EnumType(
    'FindingCommentType',
    {
        'COMMENT': 'comment',
        'OBSERVATION': 'observation'
    }
)
DELETE_FINDING_JUSTIFICATION = EnumType(
    'DeleteFindingJustification',
    {
        'DUPLICATED': 'DUPLICATED',
        'FALSE_POSITIVE': 'FALSE_POSITIVE',
        'NOT_REQUIRED': 'NOT_REQUIRED'
    }
)
ACTIONS_AFTER_BLOCKING = EnumType(
    'ActionsAfterBlocking',
    {
        'EXECUTE_OTHER_PROJECT_OTHER_CLIENT':
            'EXECUTE_OTHER_PROJECT_OTHER_CLIENT',
        'EXECUTE_OTHER_PROJECT_SAME_CLIENT':
            'EXECUTE_OTHER_PROJECT_SAME_CLIENT',
        'NONE': 'NONE',
        'OTHER': 'OTHER',
        'TRAINING': 'TRAINING'
    }
)
ACTIONS_BEFORE_BLOCKING = EnumType(
    'ActionsBeforeBlocking',
    {
        'DOCUMENT_PROJECT': 'DOCUMENT_PROJECT',
        'NONE': 'NONE',
        'OTHER': 'OTHER',
        'TEST_OTHER_PART_TOE': 'TEST_OTHER_PART_TOE',
    }
)
EVENT_ACCESSIBILITY = EnumType(
    'EventAccessibility',
    {
        'ENVIRONMENT': 'Ambiente',
        'REPOSITORY': 'Repositorio'
    }
)
AFFECTED_COMPONENTS = EnumType(
    'AffectedComponents',
    {
        'CLIENT_STATION': 'Estación de pruebas del Cliente',
        'COMPILE_ERROR': 'Error en compilación',
        'DOCUMENTATION': 'Documentación del proyecto',
        'FLUID_STATION': 'Estación de pruebas de FLUID',
        'INTERNET_CONNECTION': 'Conectividad a Internet',
        'LOCAL_CONNECTION': 'Conectividad local (LAN, WiFi)',
        'OTHER': 'Otro(s)',
        'SOURCE_CODE': 'Código fuente',
        'TEST_DATA': 'Datos de prueba',
        'TOE_ALTERATION': 'Alteración del ToE',
        'TOE_CREDENTIALS': 'Credenciales en el ToE',
        'TOE_EXCLUSSION': 'Exclusión de alcance',
        'TOE_LOCATION': 'Ubicación del ToE (IP, URL)',
        'TOE_PRIVILEGES': 'Privilegios en el ToE',
        'TOE_UNACCESSIBLE': 'Inaccesibilidad del ToE',
        'TOE_UNAVAILABLE': 'Indisponibilidad del ToE',
        'TOE_UNSTABLE': 'Inestabilidad del ToE',
        'VPN_CONNECTION': 'Conectividad VPN',
    }
)
EVENT_CONTEXT = EnumType(
    'EventContext',
    {
        'CLIENT': 'CLIENT',
        'FLUID': 'FLUID',
        'OTHER': 'OTHER',
        'PLANNING': 'PLANNING',
        'TELECOMMUTING': 'TELECOMMUTING',
    }
)
EVENT_TYPE = EnumType(
    'EventType',
    {
        'AUTHORIZATION_SPECIAL_ATTACK': 'AUTHORIZATION_SPECIAL_ATTACK',
        'CLIENT_APPROVES_CHANGE_TOE': 'CLIENT_APPROVES_CHANGE_TOE',
        'CLIENT_CANCELS_PROJECT_MILESTONE': 'CLIENT_CANCELS_PROJECT_MILESTONE',
        'CLIENT_DETECTS_ATTACK': 'CLIENT_DETECTS_ATTACK',
        'CLIENT_EXPLICITLY_SUSPENDS_PROJECT':
            'CLIENT_EXPLICITLY_SUSPENDS_PROJECT',
        'HIGH_AVAILABILITY_APPROVAL': 'HIGH_AVAILABILITY_APPROVAL',
        'INCORRECT_MISSING_SUPPLIES': 'INCORRECT_MISSING_SUPPLIES',
        'OTHER': 'OTHER',
        'TOE_DIFFERS_APPROVED': 'TOE_DIFFERS_APPROVED',
    }
)
EVENT_EVIDENCE_TYPE = EnumType(
    'EventEvidenceType',
    {
        'FILE': 'evidence_file',
        'IMAGE': 'evidence'
    }
)

REPORT_TYPE = EnumType(
    'ReportType',
    {
        'PDF': 'PDF',
        'XLS': 'XLS'
    }
)
REPORT_LANG = EnumType(
    'ReportLang',
    {
        'EN': 'en'
    }
)

CALLER_ORIGIN = EnumType(
    'CallerOrigin',
    {
        'FRONT': 'FRONT',
        'API': 'API'
    }
)

RAW_TYPES = [
    ALERT, EVENT, FINDING, FORCES_EXECUTIONS, INTERNAL_PROJECT_NAME,
    ME, PROJECT, RESOURCE, USER
]

ENUMS = [
    DELETE_VULNERABILITY_JUSTIFICATION, EVIDENCE_TYPE,
    EVIDENCE_DESCRIPTION_TYPE, SUBSCRIPTION_TYPE,
    UPDATE_CLIENT_DESCRIPTION_TREATMENT, FINDING_TYPE,
    DELETE_FINDING_JUSTIFICATION, ACTIONS_AFTER_BLOCKING,
    ACTIONS_BEFORE_BLOCKING, EVENT_ACCESSIBILITY,
    AFFECTED_COMPONENTS, EVENT_CONTEXT, EVENT_TYPE,
    EVENT_EVIDENCE_TYPE,
    REPORT_TYPE, REPORT_LANG, CALLER_ORIGIN
]

TYPES = RAW_TYPES + ENUMS
