# Standard
from typing import Tuple

# Third party
from ariadne import ObjectType

# Local
from .bill import BILL
from .bill_developer import BILL_DEVELOPER
from .consult import CONSULT
from .entity_report_subscription import ENTITY_REPORT_SUBSCRIPTION
from .execution_vulnerabilities_new import EXECUTION_VULNERABILITIES_NEW
from .execution_vulnerabilities import EXECUTION_VULNERABILITIES
from .event import EVENT
from .finding import FINDING
from .forces_executions import FORCES_EXECUTIONS
from .group import GROUP
from .internal_name import INTERNAL_NAME
from .me import ME
from .mutation import MUTATION
from .organization import ORGANIZATION
from .query import QUERY
from .resource import RESOURCE
from .stakeholder import STAKEHOLDER
from .vulnerability import VULNERABILITY


TYPES: Tuple[ObjectType, ...] = (
    BILL,
    BILL_DEVELOPER,
    CONSULT,
    ENTITY_REPORT_SUBSCRIPTION,
    EXECUTION_VULNERABILITIES_NEW,
    EXECUTION_VULNERABILITIES,
    EVENT,
    FINDING,
    FORCES_EXECUTIONS,
    GROUP,
    INTERNAL_NAME,
    ME,
    MUTATION,
    ORGANIZATION,
    QUERY,
    RESOURCE,
    STAKEHOLDER,
    VULNERABILITY
)
