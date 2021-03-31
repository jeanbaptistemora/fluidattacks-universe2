{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from tap_toe_files import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.tap-toe-files.runtime
    ];
  };
  name = "observes-bin-tap-toe-files";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
