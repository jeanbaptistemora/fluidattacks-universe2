{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from tap_zoho_analytics.converter_zoho_csv import cli";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.runtime.tap-zoho-analytics
    ];
  };
  name = "observes-bin-tap-zoho-analytics";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
