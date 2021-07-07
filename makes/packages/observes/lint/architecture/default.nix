{ makeDerivation
, path
, packages
, ...
}:
let
  paths = [
    "/observes/code_etl"
    "/observes/common/paginator"
    "/observes/common/singer_io"
    "/observes/common/utils_logger"
    "/observes/common/postgres_client"
    "/observes/etl/dif_gitlab_etl"
    "/observes/services/batch_stability"
    "/observes/services/job_last_success"
    "/observes/services/jobs_scheduler"
    "/observes/services/migrate_tables"
    "/observes/services/timedoctor_tokens"
    "/observes/singer/streamer_dynamodb"
    "/observes/singer/streamer_zoho_crm"
    "/observes/singer/tap_bugsnag"
    "/observes/singer/tap_checkly"
    "/observes/singer/tap_csv"
    "/observes/singer/tap_delighted"
    "/observes/singer/tap_formstack"
    "/observes/singer/tap_git"
    "/observes/singer/tap_gitlab"
    "/observes/singer/tap_json"
    "/observes/singer/tap_mailchimp"
    "/observes/singer/tap_mixpanel"
    "/observes/singer/tap_timedoctor"
    "/observes/singer/tap_toe_files"
    "/observes/singer/tap_zoho_analytics"
    "/observes/singer/target_redshift"
  ];
  srcs = map path paths;
in
makeDerivation {
  name = "observes-lint-architecture";
  arguments = {
    envSrc = path "/observes/architecture";
  };
  searchPaths = {
    envPythonPaths = srcs;
    envSources = [
      packages.observes.generic.linter
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_pkg_container.sh";
}
