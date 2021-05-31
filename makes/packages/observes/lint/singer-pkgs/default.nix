{ makeDerivation
, path
, packages
, ...
}:
let
  paths = [
    "/observes/singer/streamer_dynamodb"
    "/observes/singer/streamer_gitlab"
    "/observes/singer/streamer_zoho_crm"
    "/observes/singer/tap_bugsnag"
    "/observes/singer/tap_checkly"
    "/observes/singer/tap_csv"
    "/observes/singer/tap_delighted"
    "/observes/singer/tap_formstack"
    "/observes/singer/tap_git"
    "/observes/singer/tap_json"
    "/observes/singer/tap_mailchimp"
    "/observes/singer/tap_mixpanel"
    "/observes/singer/tap_timedoctor"
    "/observes/singer/tap_toe_files"
    "/observes/singer/tap_zoho_analytics"
    "/observes/singer/target_redshift"
    "/observes/singer/target_redshift_2"
  ];
  srcs = map path paths;
in
makeDerivation {
  name = "observes-lint-singer-pkgs";
  arguments = {
    envSrc = path "/observes/singer";
  };
  searchPaths = {
    envPythonPaths = srcs;
    envSources = [
      packages.observes.generic.linter
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_pkg_container.sh";
}
