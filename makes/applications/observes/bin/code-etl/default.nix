{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from code_etl.cli import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.code-etl.runtime
    ];
  };
  name = "observes-bin-code-etl";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
