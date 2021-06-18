{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from tap_gitlab.cli import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.tap-gitlab.runtime
    ];
  };
  name = "observes-bin-tap-gitlab";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
