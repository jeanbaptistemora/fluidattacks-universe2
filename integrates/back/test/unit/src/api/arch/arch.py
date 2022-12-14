from arch_lint.dag.core import (
    DAG,
    new_dag,
)
from typing import (
    Dict,
    Tuple,
    Union,
)

_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "api": ("extensions", "schema", "resolvers", "mutations", "validations"),
    "api.resolvers": (
        "vulnerability",
        "group_compliance",
        "finding",
        "organization_compliance",
        "billing",
        "credentials",
        "stakeholder",
        "me",
        "group",
        "tag",
        "event_evidence",
        "mutation_payload",
        "ip_root",
        "event",
        "toe_lines",
        "url_root",
        "query",
        "toe_port",
        "git_root",
        "git_environment_url",
        "forces_execution",
        "toe_input",
        "integration_repositories",
        "enrollment",
        "root",
        "organization_integration_repositories",
        "organization_billing",
        "organization",
        "company",
    ),
    "api.resolvers.vulnerability": (
        "treatment_justification",
        "commit_hash",
        "root_nickname",
        "specific",
        "snippet",
        "treatment_user",
        "efficacy",
        "treatment_acceptance_date",
        "tags",
        "last_state_date",
        "cycles",
        "treatment",
        "last_treatment_date",
        "finding",
        "external_bug_tracking_system",
        "report_date",
        "historic_treatment",
        "event_id",
        "hacker",
        "source",
        "where",
        "remediated",
        "last_verification_date",
        "last_reattack_requester",
        "treatment_assigned",
        "verification",
        "current_state",
        "severity",
        "historic_verification",
        "vulnerability_type",
        "tag",
        "historic_zero_risk",
        "last_reattack_date",
        "closing_date",
        "historic_state",
        "zero_risk",
        "treatment_acceptance_status",
        "treatment_changes",
        "stream",
        "last_requested_reattack_date",
    ),
    "api.resolvers.organization_compliance": (
        "standards",
        "types",
    ),
    "api.resolvers.mutation_payload": (
        "update_toe_port_payload",
        "update_toe_lines_payload",
        "update_toe_input_payload",
    ),
    "api.resolvers.integration_repositories": (
        "last_commit_date",
        "default_branch",
        "url",
    ),
    "api.resolvers.git_root": (
        "download_url",
        "last_machine_executions",
        "environment",
        "upload_url",
        "last_state_status_update",
        "includes_health_check",
        "branch",
        "use_vpn",
        "cloning_status",
        "secrets",
        "gitignore",
        "vulnerabilities",
        "credentials",
        "url",
        "environment_urls",
        "git_environment_urls",
        "last_cloning_status_update",
    ),
    "api.resolvers.stakeholder": (
        "email",
        "groups",
        "role",
        "invitation_state",
        "first_login",
        "responsibility",
        "last_login",
    ),
    "api.resolvers.organization": (
        "credentials",
        "vulnerability_grace_period",
        "min_acceptance_severity",
        "max_acceptance_severity",
        "permissions",
        "missed_authors",
        "stakeholders",
        "covered_commits",
        "max_number_acceptances",
        "missed_commits",
        "user_role",
        "organization_id",
        "integration_repositories",
        "missed_repositories",
        "max_acceptance_days",
        "company",
        "billing",
        "covered_authors",
        "compliance",
        "vulnerabilities_url",
        "min_breaking_severity",
        "integration_repositories_connection",
        "covered_repositories",
        "finding_policies",
        "groups",
        "analytics",
    ),
    "api.resolvers.tag": (
        "groups",
        "organization",
        "mean_remediate_critical_severity",
        "mean_remediate_high_severity",
        "mean_remediate_low_severity",
        "mean_remediate_medium_severity",
        "mean_remediate",
        "last_closing_date",
        "name",
        "max_open_severity",
    ),
    "api.resolvers.ip_root": ("port", "address"),
    "api.resolvers.toe_port": (
        "root",
        "attacked_by",
        "first_attack_at",
        "attacked_at",
        "has_vulnerabilities",
        "be_present_until",
        "seen_first_time_by",
        "be_present",
    ),
    "api.resolvers.toe_input": (
        "attacked_at",
        "seen_first_time_by",
        "attacked_by",
        "be_present_until",
        "root",
        "first_attack_at",
    ),
    "api.resolvers.url_root": ("protocol", "query", "path", "port", "host"),
    "api.resolvers.credentials": (
        "is_pat",
        "password",
        "organization",
        "name",
        "token",
        "is_token",
        "user",
        "key",
        "azure_organization",
        "type",
    ),
    "api.resolvers.me": (
        "access_token",
        "phone",
        "tags",
        "organizations",
        "drafts",
        "permissions",
        "has_drafts_rejected",
        "role",
        "reattacks",
        "credentials",
        "vulnerabilities_assigned",
        "tours",
        "pending_events",
        "is_concurrent_session",
        "subscriptions_to_entity_report",
        "company",
        "enrollment",
        "finding_reattacks",
        "notifications_parameters",
        "remember",
        "notifications_preferences",
    ),
    "api.resolvers.forces_execution": (
        "severity_threshold",
        "log",
        "vulnerabilities",
        "grace_period",
    ),
    "api.resolvers.root": ("nickname", "state"),
    "api.resolvers.organization_integration_repositories": (
        "last_commit_date",
        "url",
        "default_branch",
    ),
    "api.resolvers.query": (
        "groups_with_forces",
        "root",
        "events",
        "tag",
        "billing",
        "forces_executions",
        "report",
        "organization_id",
        "organization",
        "vulnerability",
        "me",
        "group",
        "resources",
        "enrollment",
        "stakeholder",
        "environment_url",
        "vulnerabilities_to_reattack",
        "list_user_groups",
        "event",
        "unfulfilled_standard_report_url",
        "finding",
        "forces_execution",
    ),
    "api.resolvers.event": (
        "accessibility",
        "hacker",
        "affected_components",
        "affected_reattacks",
        "root",
        "other_solving_reason",
        "evidence",
        "solving_reason",
        "evidence_date",
        "group_name",
        "client",
        "event_date",
        "event_id",
        "closing_date",
        "detail",
        "event_status",
        "consulting",
        "evidence_file",
        "suscription",
        "evidence_file_date",
        "historic_state",
        "event_type",
    ),
    "api.resolvers.finding": (
        "severity_score",
        "group_name",
        "closed_vulnerabilities",
        "evidence",
        "vulnerabilities_to_reattack_connection",
        "open_vulnerabilities",
        "report_date",
        "open_age",
        "remediated",
        "tracking",
        "consulting",
        "observations",
        "machine_jobs",
        "historic_state",
        "sorts",
        "treatment_summary",
        "release_date",
        "current_state",
        "zero_risk_connection",
        "is_exploitable",
        "verified",
        "last_vulnerability",
        "hacker",
        "where",
        "records",
        "verification_summary",
        "vulnerabilities_connection",
        "severity",
        "status",
        "age",
        "cvss_version",
    ),
    "api.resolvers.group_compliance": (
        "unfulfilled_standards",
        "types",
    ),
    "api.resolvers.organization_billing": ("portal", "payment_methods"),
    "api.resolvers.toe_lines": (
        "first_attack_at",
        "comments",
        "attacked_at",
        "root",
        "be_present_until",
        "attacked_lines",
        "attacked_by",
    ),
    "api.resolvers.group": (
        "closed_vulnerabilities",
        "billing",
        "events",
        "tags",
        "max_acceptance_days",
        "has_machine",
        "open_vulnerabilities",
        "credentials",
        "total_treatment",
        "max_acceptance_severity",
        "last_closed_vulnerability_finding",
        "forces_token",
        "mean_remediate_medium_severity",
        "last_closed_vulnerability",
        "has_asm",
        "toe_ports",
        "tier",
        "analytics",
        "payment_id",
        "has_forces",
        "max_open_severity_finding",
        "min_breaking_severity",
        "max_open_severity",
        "user_role",
        "mean_remediate_low_severity",
        "context",
        "has_squad",
        "language",
        "compliance",
        "consulting",
        "user_deletion",
        "subscription",
        "toe_inputs",
        "max_number_acceptances",
        "open_findings",
        "organization",
        "mean_remediate_high_severity",
        "service",
        "vulnerability_grace_period",
        "stakeholders",
        "code_languages",
        "min_acceptance_severity",
        "permissions",
        "forces_executions",
        "vulnerabilities",
        "deletion_date",
        "roots",
        "managed",
        "mean_remediate",
        "mean_remediate_critical_severity",
        "service_attributes",
        "drafts",
        "findings",
        "toe_lines",
    ),
    "api.mutations": (
        "send_assigned_notification",
        "add_toe_input",
        "unsubscribe_from_group",
        "update_payment_method",
        "update_vulnerability_description",
        "deactivate_root",
        "download_file",
        "sync_git_root",
        "remove_stakeholder",
        "remove_event_evidence",
        "add_organization",
        "add_credentials",
        "add_stakeholder",
        "add_event_consult",
        "update_git_root",
        "update_group_payment_id",
        "add_forces_execution",
        "update_toe_input",
        "remove_stakeholder_access",
        "confirm_vulnerabilities_zero_risk",
        "add_payment_method",
        "update_finding_description",
        "update_tours",
        "update_forces_access_token",
        "update_organization_stakeholder",
        "add_group_consult",
        "update_subscription",
        "remove_stakeholder_organization_access",
        "update_root_cloning_status",
        "remove_finding",
        "add_files_to_db",
        "remove_files",
        "request_vulnerabilities_zero_risk",
        "add_url_root",
        "download_billing_file",
        "update_vulnerability_treatment",
        "remove_environment_url_secret",
        "update_toe_port",
        "update_group_access_info",
        "accept_legal",
        "grant_stakeholder_access",
        "request_vulnerabilities_hold",
        "update_group_managed",
        "submit_machine_job",
        "request_groups_upgrade",
        "add_ip_root",
        "add_event",
        "download_vulnerability_file",
        "deactivate_organization_finding_policy",
        "update_evidence",
        "update_organization_policies",
        "sign_post_url",
        "remove_group",
        "add_group",
        "solve_event",
        "submit_draft",
        "handle_vulnerabilities_acceptance",
        "acknowledge_concurrent_session",
        "reject_draft",
        "add_toe_lines",
        "remove_secret",
        "remove_payment_method",
        "remove_finding_evidence",
        "start_machine_execution",
        "invalidate_access_token",
        "add_finding_consult",
        "remove_vulnerability",
        "refresh_toe_lines",
        "update_vulnerabilities_treatment",
        "reject_vulnerabilities_zero_risk",
        "finish_machine_execution",
        "add_draft",
        "remove_vulnerability_tags",
        "download_event_file",
        "add_secret",
        "request_vulnerabilities_verification",
        "update_toe_lines_sorts",
        "update_notifications_preferences",
        "update_group_stakeholder",
        "update_group_info",
        "add_group_tags",
        "add_toe_port",
        "update_evidence_description",
        "activate_root",
        "submit_group_machine_execution",
        "send_vulnerability_notification",
        "update_credentials",
        "remove_credentials",
        "add_git_root",
        "update_group_policies",
        "reject_event_solution",
        "update_ip_root",
        "update_stakeholder_phone",
        "update_access_token",
        "verify_vulnerabilities_request",
        "verify_stakeholder",
        "move_root",
        "update_group",
        "add_git_environment",
        "update_event_solving_reason",
        "remove_environment_url",
        "approve_draft",
        "handle_organization_finding_policy_acceptance",
        "add_organization_finding_policy",
        "add_enrollment",
        "upload_file",
        "submit_organization_finding_policy",
        "validate_git_access",
        "subscribe_to_entity_report",
        "update_event_evidence",
        "grant_stakeholder_organization_access",
        "update_git_environments",
        "add_machine_execution",
        "update_group_disambiguation",
        "update_severity",
        "remove_group_tag",
        "add_git_environment_secret",
        "update_url_root",
        "update_toe_lines_attacked_lines",
        "request_event_verification",
        "update_event",
    ),
    "api.schema": (
        "scalars",
        "types",
        "unions",
        "enums",
    ),
    "api.schema.types": (
        "organization_billing",
        "query",
        "vulnerability_historic_state",
        "group_compliance",
        "exploit_result",
        "trial",
        "execution_vulnerabilities",
        "verification_summary",
        "enrollment",
        "me",
        "unfulfilled_standards",
        "forces_execution",
        "group",
        "severity",
        "group_file",
        "integration_repositories",
        "prices",
        "mutation_payloads",
        "entity_report_subscription",
        "treatment_summary",
        "resource",
        "organization_compliance_standard",
        "forces_executions",
        "tracking",
        "tag",
        "toe_input",
        "report",
        "event_evidence_item",
        "toe_lines",
        "organization_compliance",
        "company",
        "finding_evidence",
        "billing",
        "credentials",
        "document_file",
        "stakeholder",
        "root",
        "requirement",
        "verification",
        "finding",
        "organization",
        "group_billing",
        "vulnerability",
        "consult",
        "toe_port",
        "event_evidence",
        "mutation",
        "event",
        "notifications_parameters",
        "treatment",
        "machine_execution",
        "snippet",
        "finding_evidence_item",
        "finding_policy",
    ),
    "api.schema.scalars": ("genericscalar", "jsonstring", "datetime"),
    "api.validations": (
        "query_breadth",
        "characters",
        "directives",
        "variables_validation",
        "query_depth",
    ),
}


def project_dag() -> DAG:
    return new_dag(_dag)