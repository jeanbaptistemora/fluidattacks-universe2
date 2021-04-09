{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from tap_delighted.cli import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.tap-delighted.runtime
    ];
  };
  name = "observes-bin-tap-delighted";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
