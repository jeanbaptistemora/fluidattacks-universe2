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
from .exploit_result import EXPLOIT_RESULT
from .finding import FINDING
from .forces_execution import FORCES_EXECUTION
from .forces_executions import FORCES_EXECUTIONS
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
from .treatment import TREATMENT
from .verification import VERIFICATION
from .vulnerability import VULNERABILITY


TYPES: Tuple[ObjectType, ...] = (
    BILL_DEVELOPER,
    BILL,
    CONSULT,
    ENTITY_REPORT_SUBSCRIPTION,
    EVENT,
    EXECUTION_VULNERABILITIES,
    EXPLOIT_RESULT,
    FINDING,
    FORCES_EXECUTION,
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
    TREATMENT,
    VERIFICATION,
    VULNERABILITY,
)
