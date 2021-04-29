{ makeDerivation
, path
, packages
, pythonFormat
, ...
}:
with packages.observes;
let
  src = path "/observes/common/postgres_client";
  formatter = pythonFormat {
    name = "observes-pkg-format";
    target = src;
  };
in
makeDerivation {
  name = "observes-lint-postgres-client";
  arguments = {
    envSrc = src;
  };
  searchPaths = {
    envPaths = [
      formatter
    ];
    envSources = [
      generic.linter
      env.postgres-client.development
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/builders/lint_and_format.sh";
}
