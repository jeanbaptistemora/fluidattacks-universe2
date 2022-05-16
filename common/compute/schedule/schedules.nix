# Schedule expressions:
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
{
  common_okta_close_sessions = {
    enabled = true;
    command = [
      "m"
      "f"
      "/common/okta/close-sessions"
    ];

    schedule_expression = "cron(0 8 * * ? *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 3600;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "common_okta_close_sessions";
      "management:area" = "cost";
      "management:product" = "common";
      "management:type" = "product";
    };
  };
  forces_process_groups_break = {
    enabled = true;
    command = [
      "m"
      "f"
      "/forces/process-groups/break"
    ];

    schedule_expression = "cron(0 9 */2 * ? *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 3600;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "forces_process_groups_break";
      "management:area" = "cost";
      "management:product" = "forces";
      "management:type" = "product";
    };
  };
  forces_process_groups_pass = {
    enabled = true;
    command = [
      "m"
      "f"
      "/forces/process-groups/pass"
    ];

    schedule_expression = "cron(0 12 * * ? *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 3600;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "forces_process_groups_pass";
      "management:area" = "cost";
      "management:product" = "forces";
      "management:type" = "product";
    };
  };
  integrates_charts_make_documents = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/charts/documents"
      "prod"
    ];

    schedule_expression = "cron(0 5,9,13 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 25;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_charts_make_documents";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_clean_ephemerals = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/back/destroy/eph"
    ];

    schedule_expression = "cron(0 9 * * ? *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 3600;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_clean_ephemerals";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_clone_groups_roots = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.clone_groups_roots.main"
    ];

    schedule_expression = "cron(0 5,8,11,14,17,21 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_clone_groups_roots";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_clone_groups_roots_vpn = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.clone_groups_roots_vpn.main"
    ];

    schedule_expression = "cron(30 6,11,16 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_clone_groups_roots_vpn";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_delete_imamura_stakeholders = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.delete_imamura_stakeholders.main"
    ];

    schedule_expression = "cron(0 1 ? * * *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_delete_imamura_stakeholders";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_delete_obsolete_groups = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.delete_obsolete_groups.main"
    ];

    schedule_expression = "cron(0 2 ? * * *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_delete_obsolete_groups";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_delete_obsolete_orgs = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.delete_obsolete_orgs.main"
    ];

    schedule_expression = "cron(0 9 ? * * *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_delete_obsolete_orgs";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_event_report = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.event_report.main"
    ];

    schedule_expression = "cron(0 14 ? * * *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_event_report";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_get_remediated_findings = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.get_remediated_findings.main"
    ];

    schedule_expression = "cron(30 5,16 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_get_remediated_findings";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_machine_queue_all = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.machine_queue_all.main"
    ];

    schedule_expression = "cron(0 5 ? * 5 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_machine_queue_all";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_machine_queue_re_attacks = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.machine_queue_re_attacks.main"
    ];

    schedule_expression = "cron(0 12,19 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_machine_queue_re_attacks";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_refresh_toe_lines = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.refresh_toe_lines.main"
    ];

    schedule_expression = "cron(0 20 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_refresh_toe_lines";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_reminder_notification = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.reminder_notification.main"
    ];

    schedule_expression = "cron(0 19 ? * * *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_reminder_notification";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_report_squad_usage = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.report_squad_usage.main"
    ];

    schedule_expression = "cron(0 18,00 ? * * *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_report_squad_usage";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_requeue_actions = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.requeue_actions.main"
    ];

    schedule_expression = "cron(15 * ? * * *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_requeue_actions";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_reset_expired_accepted_findings = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.reset_expired_accepted_findings.main"
    ];

    schedule_expression = "cron(0 0 ? * * *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_reset_expired_accepted_findings";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_review_machine_executions = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.review_machine_executions.main"
    ];

    schedule_expression = "cron(30 * ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_review_machine_executions";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_subscriptions_analytics_daily = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/subscriptions/analytics"
      "prod"
      "daily"
    ];

    schedule_expression = "cron(0 10 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_subscriptions_analytics_daily";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_subscriptions_analytics_monthly = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/subscriptions/analytics"
      "prod"
      "monthly"
    ];

    schedule_expression = "cron(0 10 1 * ? *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_subscriptions_analytics_monthly";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_subscriptions_analytics_weekly = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/subscriptions/analytics"
      "prod"
      "weekly"
    ];

    schedule_expression = "cron(0 10 ? * 2 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_subscriptions_analytics_weekly";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_subscriptions_daily_digest = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/subscriptions/daily-digest"
      "prod"
    ];

    schedule_expression = "cron(0 9 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 3600;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_subscriptions_daily_digest";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_update_group_toe_vulns = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_group_toe_vulns.main"
    ];

    schedule_expression = "cron(0 10 ? * * *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_update_group_toe_vulns";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_update_indicators = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_indicators.main"
    ];

    schedule_expression = "cron(0 9,18 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 3600;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_update_indicators";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  integrates_update_portfolios = {
    enabled = true;
    command = [
      "m"
      "f"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_portfolios.main"
    ];

    schedule_expression = "cron(0 7,14 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "integrates_update_portfolios";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
  };
  observes_etl_code_compute_bills = {
    enabled = true;
    command = [
      "m"
      "f"
      "/observes/etl/code/compute-bills"
    ];

    schedule_expression = "cron(0 2,17 * * ? *)";
    queue = "unlimited_spot";
    attempts = 2;
    timeout = 3600;
    cpu = 2;
    memory = 3600;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "observes_etl_code_compute_bills";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
  };
  observes_etl_dynamo_centralize = {
    enabled = true;
    command = [
      "m"
      "f"
      "/observes/etl/dynamo/centralize"
    ];

    schedule_expression = "cron(0 12-23/3 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 1;
    timeout = 10800;
    cpu = 1;
    memory = 1800;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "observes_etl_dynamo_centralize";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
  };
  observes_etl_mixpanel = {
    enabled = true;
    command = [
      "m"
      "f"
      "/observes/etl/mixpanel"
    ];

    schedule_expression = "cron(0 11 * * ? *)";
    queue = "unlimited_spot";
    attempts = 2;
    timeout = 86400;
    cpu = 2;
    memory = 3600;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "observes_etl_mixpanel";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
  };
  observes_etl_timedoctor = {
    enabled = true;
    command = [
      "m"
      "f"
      "/observes/etl/timedoctor"
    ];

    schedule_expression = "cron(0 9 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 2;
    timeout = 18000;
    cpu = 2;
    memory = 3600;
    parallel = 1;

    environment = [
      "CI_PROJECT_ID"
      "PRODUCT_API_TOKEN"
    ];

    tags = {
      "Name" = "observes_etl_timedoctor";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
  };
  observes_etl_timedoctor_backup = {
    enabled = true;
    command = [
      "m"
      "f"
      "/observes/etl/timedoctor/backup"
    ];

    schedule_expression = "cron(0 4 1,15 * ? *)";
    queue = "unlimited_spot";
    attempts = 4;
    timeout = 18000;
    cpu = 2;
    memory = 3600;
    parallel = 1;

    environment = [
      "CI_PROJECT_ID"
      "PRODUCT_API_TOKEN"
    ];

    tags = {
      "Name" = "observes_etl_timedoctor_backup";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
  };
  observes_etl_timedoctor_refresh_token = {
    enabled = true;
    command = [
      "m"
      "f"
      "/observes/job/timedoctor/refresh-token"
    ];

    schedule_expression = "cron(0 * * * ? *)";
    queue = "unlimited_spot";
    attempts = 1;
    timeout = 3600;
    cpu = 1;
    memory = 1800;
    parallel = 1;

    environment = [
      "CI_PROJECT_ID"
      "PRODUCT_API_TOKEN"
    ];

    tags = {
      "Name" = "observes_etl_timedoctor_refresh_token";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
  };
  observes_etl_zoho_crm_fluid = {
    enabled = true;
    command = [
      "m"
      "f"
      "/observes/etl/zoho-crm/fluid"
    ];

    schedule_expression = "cron(0 12 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 2;
    timeout = 86400;
    cpu = 2;
    memory = 3600;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "observes_etl_zoho_crm_fluid";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
  };
  observes_etl_zoho_crm_fluid_prepare = {
    enabled = true;
    command = [
      "m"
      "f"
      "/observes/etl/zoho-crm/fluid/prepare"
    ];

    schedule_expression = "cron(0 10 ? * 2-6 *)";
    queue = "unlimited_spot";
    attempts = 1;
    timeout = 3600;
    cpu = 1;
    memory = 1800;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "observes_etl_zoho_crm_fluid_prepare";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
  };
  observes_job_scheduler = {
    enabled = true;
    command = [
      "m"
      "f"
      "/observes/job/scheduler"
    ];

    schedule_expression = "cron(0 * * * ? *)";
    queue = "unlimited_spot";
    attempts = 1;
    timeout = 1800;
    cpu = 1;
    memory = 1800;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "observes_job_scheduler";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
  };
  skims_benchmark_owasp = {
    enabled = true;
    command = [
      "m"
      "f"
      "/skims/benchmark/owasp/upload"
    ];

    schedule_expression = "cron(0 11-23/2 * * ? *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 3600;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "skims_benchmark_owasp";
      "management:area" = "cost";
      "management:product" = "forces";
      "management:type" = "product";
    };
  };
  sorts_execute = {
    enabled = true;
    command = [
      "m"
      "f"
      "/sorts/execute"
    ];

    schedule_expression = "cron(0 23 ? * 7 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 86400;
    cpu = 2;
    memory = 7200;
    parallel = 15;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "sorts_execute";
      "management:area" = "cost";
      "management:product" = "sorts";
      "management:type" = "product";
    };
  };
  sorts_training_and_tune = {
    enabled = true;
    command = [
      "m"
      "f"
      "/sorts/training-and-tune"
    ];

    schedule_expression = "cron(0 5 ? * 6 *)";
    queue = "unlimited_spot";
    attempts = 3;
    timeout = 129600;
    cpu = 2;
    memory = 3600;
    parallel = 1;

    environment = ["PRODUCT_API_TOKEN"];

    tags = {
      "Name" = "sorts_training_and_tune";
      "management:area" = "cost";
      "management:product" = "sorts";
      "management:type" = "product";
    };
  };
}
