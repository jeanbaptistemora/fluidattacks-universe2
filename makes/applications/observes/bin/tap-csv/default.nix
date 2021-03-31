{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from tap_csv.cli import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.tap-csv.runtime
    ];
  };
  name = "observes-bin-tap-csv";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
