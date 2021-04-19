{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from tap_checkly.cli import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.tap-checkly.runtime
    ];
  };
  name = "observes-bin-tap-checkly";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
