{ makeDerivation
, path
, packages
, pythonFormat
, ...
}:
with packages.observes;
let
  src = path "/observes/common/singer_io";
  formatter = pythonFormat {
    name = "observes-pkg-format";
    target = src;
  };
in
makeDerivation {
  name = "observes-lint-singer-io";
  arguments = {
    envSrc = src;
  };
  searchPaths = {
    envPaths = [
      formatter
    ];
    envSources = [
      generic.linter
      env.singer-io.development
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/builders/lint_and_format.sh";
}
