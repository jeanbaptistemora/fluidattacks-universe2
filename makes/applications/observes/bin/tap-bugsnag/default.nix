{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from tap_bugsnag.cli import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.tap-bugsnag.runtime
    ];
  };
  name = "observes-bin-tap-bugsnag";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
