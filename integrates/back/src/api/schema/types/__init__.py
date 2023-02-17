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
from .group_billing import (
    GROUP_BILLING,
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
from .organization_billing import (
    ORGANIZATION_BILLING,
)
from .organization_compliance import (
    ORGANIZATION_COMPLIANCE,
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
from .vulnerability import (
    VULNERABILITY,
)
from .vulnerability_historic_state import (
    VULNERABILITY_HISTORIC_STATE,
)
from api.resolvers.billing.schema import (
    BILLING,
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
from api.schema.types.group_compliance import (
    GROUP_COMPLIANCE,
)
from api.schema.types.integration_repositories import (
    INTEGRATION_REPOSITORIES,
    ORGANIZATION_INTEGRATION_REPOSITORIES,
)
from api.schema.types.mutation_payloads import (
    UPDATE_TOE_INPUT_PAYLOAD,
    UPDATE_TOE_LINES_PAYLOAD,
    UPDATE_TOE_PORT_PAYLOAD,
)
from api.schema.types.organization_compliance_standard import (
    ORGANIZATION_COMPLIANCE_STANDARD,
)
from api.schema.types.requirement import (
    REQUIREMENT,
)
from api.schema.types.snippet import (
    SNIPPET,
)
from api.schema.types.toe_lines import (
    TOELINES,
)
from api.schema.types.toe_port import (
    TOEPORT,
)
from api.schema.types.trial import (
    TRIAL,
)
from api.schema.types.unfulfilled_standards import (
    UNFULFILLED_STANDARDS,
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
    GROUP_COMPLIANCE,
    ENVIRONMENT_URL,
    GROUP,
    GROUP_BILLING,
    GROUP_FILE,
    INTEGRATION_REPOSITORIES,
    IPROOT,
    ME,
    MUTATION,
    ORGANIZATION,
    ORGANIZATION_BILLING,
    ORGANIZATION_COMPLIANCE,
    ORGANIZATION_COMPLIANCE_STANDARD,
    ORGANIZATION_INTEGRATION_REPOSITORIES,
    PRICES,
    QUERY,
    REQUIREMENT,
    REPORT,
    RESOURCE,
    SEVERITY,
    STAKEHOLDER,
    TAG,
    TOEINPUT,
    TOELINES,
    TOEPORT,
    TRACKING,
    TREATMENT,
    TREATMENT_SUMMARY,
    TRIAL,
    SNIPPET,
    UPDATE_TOE_INPUT_PAYLOAD,
    UPDATE_TOE_LINES_PAYLOAD,
    UPDATE_TOE_PORT_PAYLOAD,
    URLROOT,
    UNFULFILLED_STANDARDS,
    VERIFICATION_SUMMARY,
    VULNERABILITY,
    VULNERABILITY_HISTORIC_STATE,
)
