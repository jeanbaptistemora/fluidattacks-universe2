{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-service-migrate-tables";
  arguments = {
    envSrc = path "/observes/services/migrate_tables";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.service-migrate-tables.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
