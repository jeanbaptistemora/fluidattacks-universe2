{ makeDerivation
, path
, packages
, pythonFormat
, ...
}:
with packages.observes;
let
  src = path "/observes/common/paginator";
  formatter = pythonFormat {
    name = "observes-pkg-format";
    target = src;
  };
in
makeDerivation {
  name = "observes-lint-paginator";
  arguments = {
    envSrc = src;
  };
  searchPaths = {
    envPaths = [
      formatter
    ];
    envSources = [
      generic.linter
      env.paginator.development
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/builders/lint_and_format.sh";
}
