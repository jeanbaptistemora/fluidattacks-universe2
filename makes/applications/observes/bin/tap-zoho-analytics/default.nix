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
      packages.observes.env.tap-zoho-analytics.runtime
    ];
  };
  name = "observes-bin-tap-zoho-analytics";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
