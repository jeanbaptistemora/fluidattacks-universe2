# Standard
from typing import Tuple

# Third party
from ariadne import EnumType

# Local
# None


ENUMS: Tuple[EnumType, ...] = (
    EnumType(
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
    ),
    EnumType(
        'ActionsBeforeBlocking',
        {
            'DOCUMENT_PROJECT': 'DOCUMENT_PROJECT',
            'NONE': 'NONE',
            'OTHER': 'OTHER',
            'TEST_OTHER_PART_TOE': 'TEST_OTHER_PART_TOE'
        }
    ),
    EnumType(
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
            'VPN_CONNECTION': 'Conectividad VPN'
        }
    ),
    EnumType(
        'AuthProvider',
        {
            'BITBUCKET': 'bitbucket',
            'GOOGLE': 'google',
            'MICROSOFT': 'microsoft'
        }
    ),
    EnumType(
        'CallerOrigin',
        {
            'API': 'API',
            'FRONT': 'FRONT'
        }
    ),
    EnumType(
        'DeleteFindingJustification',
        {
            'DUPLICATED': 'DUPLICATED',
            'FALSE_POSITIVE': 'FALSE_POSITIVE',
            'NOT_REQUIRED': 'NOT_REQUIRED'
        }
    ),
    EnumType(
        'DeleteVulnerabilityJustification',
        {
            'DUPLICATED': 'DUPLICATED',
            'FALSE_POSITIVE': 'FALSE_POSITIVE',
            'REPORTING_ERROR': 'REPORTING_ERROR'
        }
    ),
    EnumType(
        'EditGroupReason',
        {
            'BUDGET': 'BUDGET',
            'NONE': 'NONE',
            'OTHER': 'OTHER',
            'PROJECT_FINALIZATION': 'PROJECT_FINALIZATION',
            'PROJECT_SUSPENSION': 'PROJECT_SUSPENSION'
        }
    ),
    EnumType(
        'Entity',
        {
            'ORGANIZATION': 'ORGANIZATION',
            'PROJECT': 'PROJECT',
            'USER': 'USER'
        }
    ),
    EnumType(
        'EventAccessibility',
        {
            'ENVIRONMENT': 'Ambiente',
            'REPOSITORY': 'Repositorio'
        }
    ),
    EnumType(
        'EventContext',
        {
            'CLIENT': 'CLIENT',
            'FLUID': 'FLUID',
            'OTHER': 'OTHER',
            'PLANNING': 'PLANNING',
            'TELECOMMUTING': 'TELECOMMUTING'
        }
    ),
    EnumType(
        'EventEvidenceType',
        {
            'FILE': 'evidence_file',
            'IMAGE': 'evidence'
        }
    ),
    EnumType(
        'EventType',
        {
            'AUTHORIZATION_SPECIAL_ATTACK': 'AUTHORIZATION_SPECIAL_ATTACK',
            'CLIENT_APPROVES_CHANGE_TOE': 'CLIENT_APPROVES_CHANGE_TOE',
            'CLIENT_DETECTS_ATTACK': 'CLIENT_DETECTS_ATTACK',
            'HIGH_AVAILABILITY_APPROVAL': 'HIGH_AVAILABILITY_APPROVAL',
            'INCORRECT_MISSING_SUPPLIES': 'INCORRECT_MISSING_SUPPLIES',
            'OTHER': 'OTHER',
            'TOE_DIFFERS_APPROVED': 'TOE_DIFFERS_APPROVED'
        }
    ),
    EnumType(
        'EvidenceDescriptionType',
        {
            'ANIMATION': 'animation',
            'EVIDENCE1': 'evidence_route_1',
            'EVIDENCE2': 'evidence_route_2',
            'EVIDENCE3': 'evidence_route_3',
            'EVIDENCE4': 'evidence_route_4',
            'EVIDENCE5': 'evidence_route_5',
            'EXPLOITATION': 'exploitation'
        }
    ),
    EnumType(
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
    ),
    EnumType(
        'FindingConsultType',
        {
            'CONSULT': 'CONSULT',
            'OBSERVATION': 'OBSERVATION'
        }
    ),
    EnumType(
        'FindingType',
        {
            'HYGIENE': 'HYGIENE',
            'SECURITY': 'SECURITY'
        }
    ),
    EnumType(
        'Frequency',
        {
            'DAILY': 'DAILY',
            'HOURLY': 'HOURLY',
            'MONTHLY': 'MONTHLY',
            'NEVER': 'NEVER',
            'WEEKLY': 'WEEKLY'
        }
    ),
    EnumType(
        'Language',
        {
            'EN': 'en',
            'ES': 'es'
        }
    ),
    EnumType(
        'NameEntity',
        {
            'GROUP': 'GROUP',
            'ORGANIZATION': 'ORGANIZATION'
        }
    ),
    EnumType(
        'OrganizationRole',
        {
            'CUSTOMER': 'CUSTOMER',
            'CUSTOMERADMIN': 'CUSTOMERADMIN',
            'GROUP_MANAGER': 'GROUP_MANAGER'
        }
    ),
    EnumType(
        'ReportLang',
        {
            'EN': 'en'
        }
    ),
    EnumType(
        'ReportType',
        {
            'DATA': 'DATA',
            'PDF': 'PDF',
            'XLS': 'XLS'
        }
    ),
    EnumType(
        'ResourceState',
        {
            'ACTIVE': 'ACTIVE',
            'INACTIVE': 'INACTIVE'
        }
    ),
    EnumType(
        'Sorts',
        {
            'NO': 'NO',
            'YES': 'YES'
        }
    ),
    EnumType(
        'StakeholderEntity',
        {
            'ORGANIZATION': 'ORGANIZATION',
            'PROJECT': 'PROJECT'
        }
    ),
    EnumType(
        'StakeholderRole',
        {
            'ADMIN': 'admin',
            'ANALYST': 'analyst',
            'CLOSER': 'closer',
            'CUSTOMER': 'customer',
            'CUSTOMERADMIN': 'customeradmin',
            'EXECUTIVE': 'executive',
            'GROUP_MANAGER': 'group_manager',
            'RESOURCER': 'resourcer',
            'REVIEWER': 'reviewer',
            'SERVICE_FORCES': 'service_forces'
        }
    ),
    EnumType(
        'SubscriptionReportEntity',
        {
            'GROUP': 'GROUP',
            'ORGANIZATION': 'ORGANIZATION'
        }
    ),
    EnumType(
        'SubscriptionType',
        {
            'CONTINUOUS': 'continuous',
            'ONESHOT': 'oneshot'
        }
    ),
    EnumType(
        'UpdateClientDescriptionTreatment',
        {
            'ACCEPTED': 'ACCEPTED',
            'ACCEPTED_UNDEFINED': 'ACCEPTED_UNDEFINED',
            'IN_PROGRESS': 'IN PROGRESS'
        }
    ),
    EnumType(
        'VulnerabilityState',
        {
            'ACCEPTED': 'ACCEPTED',
            'CLOSED': 'CLOSED',
            'OPEN': 'OPEN',
            'UNKNOWN': 'UNKNOWN'
        }
    )
)
