from .bill import (
    BILL,
)
from .bill_author import (
    BILL_AUTHOR,
)
from .consult import (
    CONSULT,
)
from .entity_report_subscription import (
    ENTITY_REPORT_SUBSCRIPTION,
)
from .event import (
    EVENT,
)
from .execution_vulnerabilities import (
    EXECUTION_VULNERABILITIES,
)
from .exploit_result import (
    EXPLOIT_RESULT,
)
from .finding import (
    FINDING,
)
from .finding_policy import (
    FINDING_POLICY,
)
from .forces_execution import (
    FORCES_EXECUTION,
)
from .forces_executions import (
    FORCES_EXECUTIONS,
)
from .group import (
    GROUP,
)
from .internal_name import (
    INTERNAL_NAME,
)
from .me import (
    ME,
)
from .mutation import (
    MUTATION,
)
from .organization import (
    ORGANIZATION,
)
from .query import (
    QUERY,
)
from .report import (
    REPORT,
)
from .resource import (
    RESOURCE,
)
from .root import (
    GITROOT,
)
from .services_toe_lines import (
    SERVICESTOELINES,
)
from .severity import (
    SEVERITY,
)
from .stakeholder import (
    STAKEHOLDER,
)
from .tag import (
    TAG,
)
from .toe_inputs import (
    TOEINPUTS,
)
from .tracking import (
    TRACKING,
)
from .treatment import (
    TREATMENT,
)
from .treatment_summary import (
    TREATMENT_SUMMARY,
)
from .verification import (
    VERIFICATION,
)
from .vulnerability import (
    VULNERABILITY,
)
from ariadne import (
    ObjectType,
)
from typing import (
    Tuple,
)

TYPES: Tuple[ObjectType, ...] = (
    BILL_AUTHOR,
    BILL,
    CONSULT,
    ENTITY_REPORT_SUBSCRIPTION,
    EVENT,
    EXECUTION_VULNERABILITIES,
    EXPLOIT_RESULT,
    FINDING_POLICY,
    FINDING,
    FORCES_EXECUTION,
    FORCES_EXECUTIONS,
    GITROOT,
    GROUP,
    INTERNAL_NAME,
    ME,
    MUTATION,
    ORGANIZATION,
    QUERY,
    REPORT,
    RESOURCE,
    SEVERITY,
    STAKEHOLDER,
    SERVICESTOELINES,
    TAG,
    TOEINPUTS,
    TRACKING,
    TREATMENT,
    TREATMENT_SUMMARY,
    VERIFICATION,
    VULNERABILITY,
)
