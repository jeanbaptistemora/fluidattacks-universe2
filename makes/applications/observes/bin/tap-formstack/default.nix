{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from tap_formstack import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.tap-formstack.runtime
    ];
  };
  name = "observes-bin-tap-formstack";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
