from .authors import (
    AUTHORS,
)
from .billing import (
    BILLING,
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
from .finding_evidence import (
    FINDING_EVIDENCE,
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
from .group_file import (
    GROUP_FILE,
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
from .payment_method import (
    PAYMENT_METHOD,
)
from .prices import (
    PRICES,
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
    ENVIRONMENT_URL,
    GITROOT,
    IPROOT,
    URLROOT,
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
from .toe_input import (
    TOEINPUT,
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
from .vulnerability_historic_state import (
    VULNERABILITY_HISTORIC_STATE,
)
from api.schema.types.credentials import (
    CREDENTIALS,
)
from api.schema.types.event_evidence import (
    EVENT_EVIDENCE,
)
from api.schema.types.event_evidence_item import (
    EVENT_EVIDENCE_ITEM,
)
from api.schema.types.mutation_payloads import (
    UPDATE_TOE_INPUT_PAYLOAD,
    UPDATE_TOE_LINES_PAYLOAD,
)
from api.schema.types.toe_lines import (
    TOELINES,
)
from api.schema.types.verification_summary import (
    VERIFICATION_SUMMARY,
)
from ariadne import (
    ObjectType,
)
from typing import (
    Tuple,
)

TYPES: Tuple[ObjectType, ...] = (
    AUTHORS,
    BILLING,
    CONSULT,
    CREDENTIALS,
    ENTITY_REPORT_SUBSCRIPTION,
    EVENT,
    EVENT_EVIDENCE,
    EVENT_EVIDENCE_ITEM,
    EXECUTION_VULNERABILITIES,
    EXPLOIT_RESULT,
    FINDING_POLICY,
    FINDING_EVIDENCE,
    FINDING,
    FORCES_EXECUTION,
    FORCES_EXECUTIONS,
    GITROOT,
    ENVIRONMENT_URL,
    GROUP,
    GROUP_FILE,
    IPROOT,
    ME,
    MUTATION,
    ORGANIZATION,
    PAYMENT_METHOD,
    PRICES,
    QUERY,
    REPORT,
    RESOURCE,
    SEVERITY,
    STAKEHOLDER,
    TAG,
    TOEINPUT,
    TOELINES,
    TRACKING,
    TREATMENT,
    TREATMENT_SUMMARY,
    UPDATE_TOE_INPUT_PAYLOAD,
    UPDATE_TOE_LINES_PAYLOAD,
    URLROOT,
    VERIFICATION,
    VERIFICATION_SUMMARY,
    VULNERABILITY,
    VULNERABILITY_HISTORIC_STATE,
)
