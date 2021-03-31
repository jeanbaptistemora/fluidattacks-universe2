{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from migrate_tables.cli import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.runtime.migrate-tables
    ];
  };
  name = "observes-bin-service-migrate-tables";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
