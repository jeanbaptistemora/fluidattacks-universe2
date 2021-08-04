{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from tap_announcekit.cli import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.tap-announcekit.runtime
    ];
  };
  name = "observes-bin-tap-announcekit";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
