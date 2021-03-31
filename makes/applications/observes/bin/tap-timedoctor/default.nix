{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from tap_timedoctor import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.tap-timedoctor.runtime
    ];
  };
  name = "observes-bin-tap-timedoctor";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
