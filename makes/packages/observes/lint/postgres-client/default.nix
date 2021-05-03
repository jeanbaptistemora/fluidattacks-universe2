{ makeDerivation
, path
, packages
, ...
}:
with packages.observes;
makeDerivation {
  name = "observes-lint-postgres-client";
  arguments = {
    envSrc = path "/observes/common/postgres_client";
  };
  searchPaths = {
    envSources = [
      generic.linter
      env.postgres-client.development
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
