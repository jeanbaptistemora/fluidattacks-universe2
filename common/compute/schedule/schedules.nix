# Schedule expressions:
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
{
  forces_process_groups_break = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/forces/process-groups/break"
    ];

    schedule_expression = "cron(0 9 */2 * ? *)";
    size = "nano";
    awsRole = "prod_forces";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "forces_process_groups_break";
      "Management:Area" = "cost";
      "Management:Product" = "forces";
      "Management:Type" = "product";
    };
  };
  forces_process_groups_pass = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/forces/process-groups/pass"
    ];

    schedule_expression = "cron(0 12 * * ? *)";
    size = "nano";
    awsRole = "prod_forces";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "forces_process_groups_pass";
      "Management:Area" = "cost";
      "Management:Product" = "forces";
      "Management:Type" = "product";
    };
  };
  integrates_clean_ephemerals = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/back/destroy/eph"
    ];

    schedule_expression = "cron(0 9 * * ? *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_clean_ephemerals";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_clone_groups_roots = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.clone_groups_roots.main"
    ];

    schedule_expression = "cron(0 5,8,11,14,17,21 ? * 2-6 *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_clone_groups_roots";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_clone_groups_roots_vpn = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.clone_groups_roots_vpn.main"
    ];

    schedule_expression = "cron(30 6,11,16 ? * 2-6 *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_clone_groups_roots_vpn";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_consume_dynamodb_stream = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/streams"
      "prod"
      "dynamodb"
    ];

    schedule_expression = "cron(0/30 * * * ? *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 1;
    timeout = 1200;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_consume_dynamodb_stream";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_groups_languages_distribution = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.groups_languages_distribution.main"
    ];

    schedule_expression = "cron(0,30 0 ? * 2,5 *)";
    size = "small";
    awsRole = "prod_integrates";
    attempts = 1;
    timeout = 21600;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "INTEGRATES_API_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_groups_languages_distribution";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_organization_vulnerabilities = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.organization_vulnerabilities.main"
    ];

    schedule_expression = "cron(30 1,5,9,13,17,21 * * ? *)";
    size = "medium";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 43200;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_organization_vulnerabilities";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_delete_imamura_stakeholders = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.delete_imamura_stakeholders.main"
    ];

    schedule_expression = "cron(0 1 ? * * *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_delete_imamura_stakeholders";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_delete_obsolete_groups = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.delete_obsolete_groups.main"
    ];

    schedule_expression = "cron(0 2 ? * * *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_delete_obsolete_groups";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_delete_obsolete_orgs = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.delete_obsolete_orgs.main"
    ];

    schedule_expression = "cron(0 9 ? * * *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_delete_obsolete_orgs";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_event_report = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.event_report.main"
    ];

    schedule_expression = "cron(0 14 ? * * *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_event_report";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_missing_environment_alert = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.missing_environment_alert.main"
    ];

    schedule_expression = "cron(0 11 ? * * *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_missing_environment_alert";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_numerator_report_digest = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.numerator_report_digest.main"
    ];

    schedule_expression = "cron(0 11 ? * 2-6 *)";
    size = "large";
    awsRole = "prod_integrates";
    attempts = 1;
    timeout = 129600;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_numerator_report_digest";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_get_remediated_findings = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.get_remediated_findings.main"
    ];

    schedule_expression = "cron(30 5,16 ? * 2-6 *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_get_remediated_findings";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_machine_queue_all = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.machine_queue_all.main"
    ];

    schedule_expression = "cron(0 5 ? * 5 *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_machine_queue_all";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_machine_queue_re_attacks = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.machine_queue_re_attacks.main"
    ];

    schedule_expression = "cron(0 12,19 ? * 2-6 *)";
    size = "small";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_machine_queue_re_attacks";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_machine_report = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.report_machine.main"
    ];

    schedule_expression = "cron(0/10 7-21 ? * 2-6 *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 3600;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_machine_report";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_refresh_toe_lines = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.refresh_toe_lines.main"
    ];

    schedule_expression = "cron(0 20 ? * 2-6 *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_refresh_toe_lines";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_reminder_notification = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.reminder_notification.main"
    ];

    schedule_expression = "cron(0 19 ? * * *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_reminder_notification";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_report_squad_usage = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.report_squad_usage.main"
    ];

    schedule_expression = "cron(0 18,00 ? * * *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_report_squad_usage";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_requeue_actions = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.requeue_actions.main"
    ];

    schedule_expression = "cron(15 * ? * * *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_requeue_actions";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_reset_expired_accepted_findings = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.reset_expired_accepted_findings.main"
    ];

    schedule_expression = "cron(0 0 ? * * *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_reset_expired_accepted_findings";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_review_machine_executions = {
    enabled = false;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.review_machine_executions.main"
    ];

    schedule_expression = "cron(30 * ? * 2-6 *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_review_machine_executions";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_send_deprecation_notice = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.send_deprecation_notice.main"
    ];

    schedule_expression = "cron(0 12 12 * ? *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_send_deprecation_notice";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_subscriptions_analytics_daily = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/subscriptions/analytics"
      "prod"
      "daily"
    ];

    schedule_expression = "cron(0 10 ? * 2-6 *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_subscriptions_analytics_daily";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_subscriptions_analytics_monthly = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/subscriptions/analytics"
      "prod"
      "monthly"
    ];

    schedule_expression = "cron(0 10 1 * ? *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_subscriptions_analytics_monthly";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_subscriptions_analytics_weekly = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/subscriptions/analytics"
      "prod"
      "weekly"
    ];

    schedule_expression = "cron(0 10 ? * 2 *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_subscriptions_analytics_weekly";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_temporal_treatment_report = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.temporal_treatment_report.main"
    ];

    schedule_expression = "cron(0 15 ? * * *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_temporal_treatment_report";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_update_group_toe_vulns = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_group_toe_vulns.main"
    ];

    schedule_expression = "cron(0 10 ? * * *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_update_group_toe_vulns";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_update_indicators = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_indicators.main"
    ];

    schedule_expression = "cron(0 9,18 ? * 2-6 *)";
    size = "small";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 129600;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_update_indicators";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  integrates_update_portfolios = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_portfolios.main"
    ];

    schedule_expression = "cron(0 7,14 ? * 2-6 *)";
    size = "nano";
    awsRole = "prod_integrates";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "integrates_update_portfolios";
      "Management:Area" = "cost";
      "Management:Product" = "integrates";
      "Management:Type" = "product";
    };
  };
  observes_etl_code_compute_bills = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/code/compute-bills"
    ];

    schedule_expression = "cron(0 2,17 * * ? *)";
    size = "nano";
    awsRole = "prod_observes";
    attempts = 2;
    timeout = 3600;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "observes_etl_code_compute_bills";
      "Management:Area" = "cost";
      "Management:Product" = "observes";
      "Management:Type" = "product";
    };
  };
  observes_etl_dynamo_centralize = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/dynamo/centralize"
    ];

    schedule_expression = "cron(0 12-23/3 ? * 2-6 *)";
    size = "nano";
    awsRole = "prod_observes";
    attempts = 1;
    timeout = 10800;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "observes_etl_dynamo_centralize";
      "Management:Area" = "cost";
      "Management:Product" = "observes";
      "Management:Type" = "product";
    };
  };
  observes_etl_gitlab_ephemeral = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/gitlab/universe/ephemeral"
    ];

    schedule_expression = "cron(0 11 ? * 1-5 *)";
    size = "nano";
    awsRole = "prod_observes";
    attempts = 1;
    timeout = 10800;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "observes_etl_gitlab_issues";
      "Management:Area" = "cost";
      "Management:Product" = "observes";
      "Management:Type" = "product";
    };
  };
  observes_etl_mixpanel = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/mixpanel"
    ];

    schedule_expression = "cron(0 11 * * ? *)";
    size = "small";
    awsRole = "prod_observes";
    attempts = 2;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "observes_etl_mixpanel";
      "Management:Area" = "cost";
      "Management:Product" = "observes";
      "Management:Type" = "product";
    };
  };
  observes_etl_timedoctor = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/timedoctor"
    ];

    schedule_expression = "cron(0 9 ? * 2-6 *)";
    size = "nano";
    awsRole = "prod_observes";
    attempts = 2;
    timeout = 18000;
    parallel = 1;

    environment = [
      "CI_PROJECT_ID"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "observes_etl_timedoctor";
      "Management:Area" = "cost";
      "Management:Product" = "observes";
      "Management:Type" = "product";
    };
  };
  observes_etl_timedoctor_backup = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/timedoctor/backup"
    ];

    schedule_expression = "cron(0 4 1,15 * ? *)";
    size = "nano";
    awsRole = "prod_observes";
    attempts = 4;
    timeout = 18000;
    parallel = 1;

    environment = [
      "CI_PROJECT_ID"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "observes_etl_timedoctor_backup";
      "Management:Area" = "cost";
      "Management:Product" = "observes";
      "Management:Type" = "product";
    };
  };
  observes_etl_zoho_crm_fluid = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/zoho-crm/fluid"
    ];

    schedule_expression = "cron(0 12 ? * 2-6 *)";
    size = "nano";
    awsRole = "prod_observes";
    attempts = 2;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "observes_etl_zoho_crm_fluid";
      "Management:Area" = "cost";
      "Management:Product" = "observes";
      "Management:Type" = "product";
    };
  };
  observes_etl_zoho_crm_fluid_prepare = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/zoho-crm/fluid/prepare"
    ];

    schedule_expression = "cron(0 10 ? * 2-6 *)";
    size = "nano";
    awsRole = "prod_observes";
    attempts = 1;
    timeout = 3600;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "observes_etl_zoho_crm_fluid_prepare";
      "Management:Area" = "cost";
      "Management:Product" = "observes";
      "Management:Type" = "product";
    };
  };
  observes_job_scheduler = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/job/scheduler"
    ];

    schedule_expression = "cron(0 * * * ? *)";
    size = "nano";
    awsRole = "prod_observes";
    attempts = 1;
    timeout = 3600;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "observes_job_scheduler";
      "Management:Area" = "cost";
      "Management:Product" = "observes";
      "Management:Type" = "product";
    };
  };
  skims_benchmark_owasp = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/skims/benchmark/owasp/upload"
    ];

    schedule_expression = "cron(0 11-23/2 * * ? *)";
    size = "nano";
    awsRole = "prod_skims";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "skims_benchmark_owasp";
      "Management:Area" = "cost";
      "Management:Product" = "skims";
      "Management:Type" = "product";
    };
  };
  skims_update_sca_table = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/skims/sca/scheduler"
      "schedulers.update_sca_table.main"
    ];

    schedule_expression = "cron(0 10 * * ? *)";
    size = "nano";
    awsRole = "prod_skims";
    attempts = 3;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "skims_update_sca_table";
      "Management:Area" = "cost";
      "Management:Product" = "skims";
      "Management:Type" = "product";
    };
  };
  sorts_association_rules = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/sorts/association-rules/bin"
    ];

    schedule_expression = "cron(0 0 1 1-12/3 ? *)";
    size = "large";
    awsRole = "prod_sorts";
    attempts = 1;
    timeout = 86400;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "sorts_association_rules";
      "Management:Area" = "cost";
      "Management:Product" = "sorts";
      "Management:Type" = "product";
    };
  };
  sorts_association_execute = rec {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/sorts/association-execute"
      (toString parallel)
    ];

    schedule_expression = "cron(0 23 ? * 7 *)";
    size = "nano";
    awsRole = "prod_sorts";
    attempts = 3;
    timeout = 86400;
    parallel = 15;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "sorts_association_execute";
      "Management:Area" = "cost";
      "Management:Product" = "sorts";
      "Management:Type" = "product";
    };
  };
  sorts_execute = rec {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/sorts/execute"
      (toString parallel)
    ];

    schedule_expression = "cron(0 23 ? * 7 *)";
    size = "nano";
    awsRole = "prod_sorts";
    attempts = 3;
    timeout = 86400;
    parallel = 15;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "sorts_execute";
      "Management:Area" = "cost";
      "Management:Product" = "sorts";
      "Management:Type" = "product";
    };
  };
  sorts_training_and_tune = {
    enabled = true;
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/sorts/training-and-tune"
    ];

    schedule_expression = "cron(0 5 ? * 6 *)";
    size = "nano";
    awsRole = "prod_sorts";
    attempts = 3;
    timeout = 129600;
    parallel = 1;

    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];

    tags = {
      "Name" = "sorts_training_and_tune";
      "Management:Area" = "cost";
      "Management:Product" = "sorts";
      "Management:Type" = "product";
    };
  };
}
