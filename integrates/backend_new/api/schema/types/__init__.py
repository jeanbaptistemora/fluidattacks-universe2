# Standard
from typing import Tuple

# Third party
from ariadne import ObjectType

# Local
from .bill import BILL
from .bill_developer import BILL_DEVELOPER
from .consult import CONSULT
from .entity_report_subscription import ENTITY_REPORT_SUBSCRIPTION
from .event import EVENT
from .execution_vulnerabilities import EXECUTION_VULNERABILITIES
from .execution_vulnerabilities_new import EXECUTION_VULNERABILITIES_NEW
from .exploit_result import EXPLOIT_RESULT
from .finding import FINDING
from .forces_execution import FORCES_EXECUTION
from .forces_execution_new import FORCES_EXECUTION_NEW
from .forces_executions import FORCES_EXECUTIONS
from .forces_executions_new import FORCES_EXECUTIONS_NEW
from .group import GROUP
from .internal_name import INTERNAL_NAME
from .me import ME
from .mutation import MUTATION
from .organization import ORGANIZATION
from .query import QUERY
from .report import REPORT
from .resource import RESOURCE
from .stakeholder import STAKEHOLDER
from .tag import TAG
from .verification import VERIFICATION
from .vulnerability import VULNERABILITY


TYPES: Tuple[ObjectType, ...] = (
    BILL_DEVELOPER,
    BILL,
    CONSULT,
    ENTITY_REPORT_SUBSCRIPTION,
    EVENT,
    EXECUTION_VULNERABILITIES_NEW,
    EXECUTION_VULNERABILITIES,
    EXPLOIT_RESULT,
    FINDING,
    FORCES_EXECUTION_NEW,
    FORCES_EXECUTION,
    FORCES_EXECUTIONS_NEW,
    FORCES_EXECUTIONS,
    GROUP,
    INTERNAL_NAME,
    ME,
    MUTATION,
    ORGANIZATION,
    QUERY,
    REPORT,
    RESOURCE,
    STAKEHOLDER,
    TAG,
    VERIFICATION,
    VULNERABILITY
)
