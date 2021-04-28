{ makeDerivation
, path
, packages
, pythonFormat
, ...
}:
with packages.observes;
let
  src = path "/observes/singer/tap_checkly";
  formatter = pythonFormat {
    name = "observes-pkg-format";
    target = src;
  };
in
makeDerivation {
  name = "observes-lint-tap-checkly";
  arguments = {
    envSrc = src;
  };
  searchPaths = {
    envPaths = [
      formatter
    ];
    envSources = [
      generic.linter
      env.tap-checkly.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/builders/lint_and_format.sh";
}
