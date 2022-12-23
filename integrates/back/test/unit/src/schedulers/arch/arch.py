from arch_lint.dag import (
    DagMap,
)
from typing import (
    Dict,
    Tuple,
    Union,
)

_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "schedulers": (
        "groups_languages_distribution",
        "reminder_notification",
        "consulting_digest_notification",
        "organization_vulnerabilities",
        "event_report",
        "reset_expired_accepted_findings",
        "machine_queue_all",
        "delete_imamura_stakeholders",
        "update_organization_overview",
        "delete_obsolete_orgs",
        "review_machine_executions",
        "abandoned_trial_notification",
        "temporal_treatment_report",
        "users_weekly_report",
        "requeue_actions",
        "update_group_toe_vulns",
        "send_trial_engagement_notification",
        "fix_machine_executions",
        "treatment_alert_notification",
        "refresh_toe_lines",
        "report_squad_usage",
        "expire_free_trial",
        "numerator_report_digest",
        "machine_queue_re_attacks",
        "missing_environment_alert",
        "update_indicators",
        "send_deprecation_notice",
        "update_portfolios",
        "clone_groups_roots_vpn",
        "update_compliance",
        "update_organization_repositories",
        "delete_obsolete_groups",
        "clone_groups_roots",
        "common",
    ),
}


def project_dag() -> DagMap:
    result = DagMap.new(_dag)
    if isinstance(result, Exception):
        raise result  # pylint: disable=raising-bad-type
    return result
