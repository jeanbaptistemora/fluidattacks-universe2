from api.mutations.payloads.update_toe_input_payload import (
    UPDATE_TOE_INPUT_PAYLOAD,
)
from api.mutations.payloads.update_toe_lines_payload import (
    UPDATE_TOE_LINES_PAYLOAD,
)
from api.mutations.payloads.update_toe_port_payload import (
    UPDATE_TOE_PORT_PAYLOAD,
)
from api.mutations.schema import (
    MUTATION,
)
from api.resolvers.billing.schema import (
    BILLING,
)
from api.resolvers.code_languages.schema import (
    CODE_LANGUAGES,
)
from api.resolvers.consult.schema import (
    CONSULT,
)
from api.resolvers.credentials.schema import (
    CREDENTIALS,
)
from api.resolvers.entity_report_subscription.schema import (
    ENTITY_REPORT_SUBSCRIPTION,
)
from api.resolvers.event.schema import (
    EVENT,
)
from api.resolvers.event_evidence.schema import (
    EVENT_EVIDENCE,
)
from api.resolvers.event_evidence_item.schema import (
    EVENT_EVIDENCE_ITEM,
)
from api.resolvers.execution_edge.schema import (
    EXECUTION_EDGE,
)
from api.resolvers.execution_vulnerabilities.schema import (
    EXECUTION_VULNERABILITIES,
)
from api.resolvers.executions_connection.schema import (
    EXECUTIONS_CONNECTION,
)
from api.resolvers.exploit_result.schema import (
    EXPLOIT_RESULT,
)
from api.resolvers.finding.schema import (
    FINDING,
)
from api.resolvers.finding_evidence.schema import (
    FINDING_EVIDENCE,
)
from api.resolvers.finding_policy.schema import (
    FINDING_POLICY,
)
from api.resolvers.forces_execution.schema import (
    FORCES_EXECUTION,
)
from api.resolvers.forces_executions.schema import (
    FORCES_EXECUTIONS,
)
from api.resolvers.git_environment_url.schema import (
    GIT_ENVIRONMENT_URL,
)
from api.resolvers.git_root.schema import (
    GIT_ROOT,
)
from api.resolvers.git_root_cloning_status.schema import (
    GIT_ROOT_CLONING_STATUS,
)
from api.resolvers.group.schema import (
    GROUP,
)
from api.resolvers.group_billing.schema import (
    GROUP_BILLING,
)
from api.resolvers.group_billing_author.schema import (
    GROUP_BILLING_AUTHOR,
)
from api.resolvers.group_compliance.schema import (
    GROUP_COMPLIANCE,
)
from api.resolvers.group_file.schema import (
    GROUP_FILE,
)
from api.resolvers.integration_repositories.schema import (
    INTEGRATION_REPOSITORIES,
)
from api.resolvers.integration_repositories_connection.schema import (
    INTEGRATION_REPOSITORIES_CONNECTION,
)
from api.resolvers.integration_repositories_edge.schema import (
    INTEGRATION_REPOSITORIES_EDGE,
)
from api.resolvers.ip_root.schema import (
    IP_ROOT,
)
from api.resolvers.machine_job.schema import (
    MACHINE_JOB,
)
from api.resolvers.me.schema import (
    ME,
)
from api.resolvers.notifications_parameters.schema import (
    NOTIFICATIONS_PARAMETERS,
)
from api.resolvers.notifications_preferences.schema import (
    NOTIFICATIONS_PREFERENCES,
)
from api.resolvers.organization.schema import (
    ORGANIZATION,
)
from api.resolvers.organization_billing.schema import (
    ORGANIZATION_BILLING,
)
from api.resolvers.organization_billing_active_group.schema import (
    ORGANIZATION_BILLING_ACTIVE_GROUP,
)
from api.resolvers.organization_billing_author.schema import (
    ORGANIZATION_BILLING_AUTHOR,
)
from api.resolvers.organization_compliance.schema import (
    ORGANIZATION_COMPLIANCE,
)
from api.resolvers.organization_compliance_standard.schema import (
    ORGANIZATION_COMPLIANCE_STANDARD,
)
from api.resolvers.organization_integration_repositories.schema import (
    ORGANIZATION_INTEGRATION_REPOSITORIES,
)
from api.resolvers.page_info.schema import (
    PAGE_INFO,
)
from api.resolvers.payment_method.schema import (
    PAYMENT_METHOD,
)
from api.resolvers.phone.schema import (
    PHONE,
)
from api.resolvers.price.schema import (
    PRICE,
)
from api.resolvers.prices.schema import (
    PRICES,
)
from api.resolvers.query.schema import (
    QUERY,
)
from api.resolvers.report.schema import (
    REPORT,
)
from api.resolvers.requirement.schema import (
    REQUIREMENT,
)
from api.resolvers.resource.schema import (
    RESOURCE,
)
from api.resolvers.secret.schema import (
    SECRET,
)
from api.resolvers.severity.schema import (
    SEVERITY,
)
from api.resolvers.snippet.schema import (
    SNIPPET,
)
from api.resolvers.stakeholder.schema import (
    STAKEHOLDER,
)
from api.resolvers.tag.schema import (
    TAG,
)
from api.resolvers.toe_input.schema import (
    TOE_INPUT,
)
from api.resolvers.toe_input_edge.schema import (
    TOE_INPUT_EDGE,
)
from api.resolvers.toe_inputs_connection.schema import (
    TOE_INPUTS_CONNECTION,
)
from api.resolvers.toe_lines.schema import (
    TOE_LINES,
)
from api.resolvers.toe_lines_connection.schema import (
    TOE_LINES_CONNECTION,
)
from api.resolvers.toe_lines_edge.schema import (
    TOE_LINES_EDGE,
)
from api.resolvers.toe_lines_sort_suggestion.schema import (
    TOE_LINES_SORT_SUGGESTION,
)
from api.resolvers.toe_port.schema import (
    TOE_PORT,
)
from api.resolvers.toe_port_edge.schema import (
    TOE_PORT_EDGE,
)
from api.resolvers.toe_ports_connection.schema import (
    TOE_PORTS_CONNECTION,
)
from api.resolvers.tours.schema import (
    TOURS,
)
from api.resolvers.tracking.schema import (
    TRACKING,
)
from api.resolvers.treatment.schema import (
    TREATMENT,
)
from api.resolvers.treatment_summary.schema import (
    TREATMENT_SUMMARY,
)
from api.resolvers.trial.schema import (
    TRIAL,
)
from api.resolvers.unfulfilled_standard.schema import (
    UNFULFILLED_STANDARD,
)
from api.resolvers.url_root.schema import (
    URL_ROOT,
)
from api.resolvers.verification_summary.schema import (
    VERIFICATION_SUMMARY,
)
from api.resolvers.vulnerabilities_summary.schema import (
    VULNERABILITIES_SUMMARY,
)
from api.resolvers.vulnerability.schema import (
    VULNERABILITY,
)
from api.resolvers.vulnerability_historic_state.schema import (
    VULNERABILITY_HISTORIC_STATE,
)
from ariadne import (
    ObjectType,
)
from typing import (
    Tuple,
)

TYPES: Tuple[ObjectType, ...] = (
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
