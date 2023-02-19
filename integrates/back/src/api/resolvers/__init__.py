from ..mutations.payloads.update_toe_input_payload import (
    UPDATE_TOE_INPUT_PAYLOAD,
)
from ..mutations.payloads.update_toe_lines_payload import (
    UPDATE_TOE_LINES_PAYLOAD,
)
from ..mutations.payloads.update_toe_port_payload import (
    UPDATE_TOE_PORT_PAYLOAD,
)
from ..mutations.schema import (
    MUTATION,
)
from .billing.schema import (
    BILLING,
)
from .code_languages.schema import (
    CODE_LANGUAGES,
)
from .consult.schema import (
    CONSULT,
)
from .credentials.schema import (
    CREDENTIALS,
)
from .entity_report_subscription.schema import (
    ENTITY_REPORT_SUBSCRIPTION,
)
from .event.schema import (
    EVENT,
)
from .event_evidence.schema import (
    EVENT_EVIDENCE,
)
from .event_evidence_item.schema import (
    EVENT_EVIDENCE_ITEM,
)
from .execution_edge.schema import (
    EXECUTION_EDGE,
)
from .execution_vulnerabilities.schema import (
    EXECUTION_VULNERABILITIES,
)
from .executions_connection.schema import (
    EXECUTIONS_CONNECTION,
)
from .exploit_result.schema import (
    EXPLOIT_RESULT,
)
from .finding.schema import (
    FINDING,
)
from .finding_evidence.schema import (
    FINDING_EVIDENCE,
)
from .finding_policy.schema import (
    FINDING_POLICY,
)
from .forces_execution.schema import (
    FORCES_EXECUTION,
)
from .forces_executions.schema import (
    FORCES_EXECUTIONS,
)
from .git_environment_url.schema import (
    GIT_ENVIRONMENT_URL,
)
from .git_root.schema import (
    GIT_ROOT,
)
from .git_root_cloning_status.schema import (
    GIT_ROOT_CLONING_STATUS,
)
from .group.schema import (
    GROUP,
)
from .group_billing.schema import (
    GROUP_BILLING,
)
from .group_billing_author.schema import (
    GROUP_BILLING_AUTHOR,
)
from .group_compliance.schema import (
    GROUP_COMPLIANCE,
)
from .group_file.schema import (
    GROUP_FILE,
)
from .integration_repositories.schema import (
    INTEGRATION_REPOSITORIES,
)
from .integration_repositories_connection.schema import (
    INTEGRATION_REPOSITORIES_CONNECTION,
)
from .integration_repositories_edge.schema import (
    INTEGRATION_REPOSITORIES_EDGE,
)
from .ip_root.schema import (
    IP_ROOT,
)
from .machine_job.schema import (
    MACHINE_JOB,
)
from .me.schema import (
    ME,
)
from .notifications_parameters.schema import (
    NOTIFICATIONS_PARAMETERS,
)
from .notifications_preferences.schema import (
    NOTIFICATIONS_PREFERENCES,
)
from .organization.schema import (
    ORGANIZATION,
)
from .organization_billing.schema import (
    ORGANIZATION_BILLING,
)
from .organization_billing_active_group.schema import (
    ORGANIZATION_BILLING_ACTIVE_GROUP,
)
from .organization_billing_author.schema import (
    ORGANIZATION_BILLING_AUTHOR,
)
from .organization_compliance.schema import (
    ORGANIZATION_COMPLIANCE,
)
from .organization_compliance_standard.schema import (
    ORGANIZATION_COMPLIANCE_STANDARD,
)
from .organization_integration_repositories.schema import (
    ORGANIZATION_INTEGRATION_REPOSITORIES,
)
from .page_info.schema import (
    PAGE_INFO,
)
from .payment_method.schema import (
    PAYMENT_METHOD,
)
from .phone.schema import (
    PHONE,
)
from .price.schema import (
    PRICE,
)
from .prices.schema import (
    PRICES,
)
from .query.schema import (
    QUERY,
)
from .report.schema import (
    REPORT,
)
from .requirement.schema import (
    REQUIREMENT,
)
from .resource.schema import (
    RESOURCE,
)
from .secret.schema import (
    SECRET,
)
from .severity.schema import (
    SEVERITY,
)
from .snippet.schema import (
    SNIPPET,
)
from .stakeholder.schema import (
    STAKEHOLDER,
)
from .tag.schema import (
    TAG,
)
from .toe_input.schema import (
    TOE_INPUT,
)
from .toe_input_edge.schema import (
    TOE_INPUT_EDGE,
)
from .toe_inputs_connection.schema import (
    TOE_INPUTS_CONNECTION,
)
from .toe_lines.schema import (
    TOE_LINES,
)
from .toe_lines_connection.schema import (
    TOE_LINES_CONNECTION,
)
from .toe_lines_edge.schema import (
    TOE_LINES_EDGE,
)
from .toe_lines_sort_suggestion.schema import (
    TOE_LINES_SORT_SUGGESTION,
)
from .toe_port.schema import (
    TOE_PORT,
)
from .toe_port_edge.schema import (
    TOE_PORT_EDGE,
)
from .toe_ports_connection.schema import (
    TOE_PORTS_CONNECTION,
)
from .tours.schema import (
    TOURS,
)
from .tracking.schema import (
    TRACKING,
)
from .treatment.schema import (
    TREATMENT,
)
from .treatment_summary.schema import (
    TREATMENT_SUMMARY,
)
from .trial.schema import (
    TRIAL,
)
from .unfulfilled_standard.schema import (
    UNFULFILLED_STANDARD,
)
from .url_root.schema import (
    URL_ROOT,
)
from .verification_summary.schema import (
    VERIFICATION_SUMMARY,
)
from .vulnerabilities_summary.schema import (
    VULNERABILITIES_SUMMARY,
)
from .vulnerability.schema import (
    VULNERABILITY,
)
from .vulnerability_historic_state.schema import (
    VULNERABILITY_HISTORIC_STATE,
)
from ariadne import (
    ObjectType,
)

TYPES: tuple[ObjectType, ...] = (
    BILLING,
    CODE_LANGUAGES,
    CONSULT,
    CREDENTIALS,
    ENTITY_REPORT_SUBSCRIPTION,
    EVENT,
    EVENT_EVIDENCE,
    EVENT_EVIDENCE_ITEM,
    EXECUTION_EDGE,
    EXECUTION_VULNERABILITIES,
    EXECUTIONS_CONNECTION,
    EXPLOIT_RESULT,
    FINDING_POLICY,
    FINDING_EVIDENCE,
    FINDING,
    FORCES_EXECUTION,
    FORCES_EXECUTIONS,
    GIT_ROOT,
    GROUP_COMPLIANCE,
    GIT_ENVIRONMENT_URL,
    GIT_ROOT_CLONING_STATUS,
    GROUP,
    GROUP_BILLING,
    GROUP_BILLING_AUTHOR,
    GROUP_FILE,
    INTEGRATION_REPOSITORIES,
    INTEGRATION_REPOSITORIES_CONNECTION,
    INTEGRATION_REPOSITORIES_EDGE,
    IP_ROOT,
    MACHINE_JOB,
    ME,
    MUTATION,
    NOTIFICATIONS_PARAMETERS,
    NOTIFICATIONS_PREFERENCES,
    ORGANIZATION,
    ORGANIZATION_BILLING,
    ORGANIZATION_BILLING_ACTIVE_GROUP,
    ORGANIZATION_BILLING_AUTHOR,
    ORGANIZATION_COMPLIANCE,
    ORGANIZATION_COMPLIANCE_STANDARD,
    ORGANIZATION_INTEGRATION_REPOSITORIES,
    PAGE_INFO,
    PAYMENT_METHOD,
    PHONE,
    PRICE,
    PRICES,
    QUERY,
    REPORT,
    REQUIREMENT,
    RESOURCE,
    SEVERITY,
    STAKEHOLDER,
    TAG,
    TOE_INPUT,
    TOE_INPUT_EDGE,
    TOE_INPUTS_CONNECTION,
    TOE_LINES,
    TOE_LINES_CONNECTION,
    TOE_LINES_EDGE,
    TOE_LINES_SORT_SUGGESTION,
    TOE_PORT,
    TOE_PORT_EDGE,
    TOE_PORTS_CONNECTION,
    TOURS,
    TRACKING,
    TREATMENT,
    TREATMENT_SUMMARY,
    TRIAL,
    SECRET,
    SNIPPET,
    UPDATE_TOE_INPUT_PAYLOAD,
    UPDATE_TOE_LINES_PAYLOAD,
    UPDATE_TOE_PORT_PAYLOAD,
    URL_ROOT,
    UNFULFILLED_STANDARD,
    VERIFICATION_SUMMARY,
    VULNERABILITIES_SUMMARY,
    VULNERABILITY,
    VULNERABILITY_HISTORIC_STATE,
)
