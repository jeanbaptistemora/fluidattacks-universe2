{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from tap_json.cli import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.tap-json.runtime
    ];
  };
  name = "observes-tap-json";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
