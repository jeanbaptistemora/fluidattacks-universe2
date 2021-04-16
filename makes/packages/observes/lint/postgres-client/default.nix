{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-postgres-client";
  arguments = {
    envSrc = path "/observes/common/postgres_client";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.postgres-client.development
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
