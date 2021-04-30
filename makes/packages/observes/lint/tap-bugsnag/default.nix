{ makeDerivation
, path
, packages
, pythonFormat
, ...
}:
with packages.observes;
let
  src = path "/observes/singer/tap_bugsnag";
  formatter = pythonFormat {
    name = "observes-pkg-format";
    targets = [ src ];
  };
in
makeDerivation {
  name = "observes-lint-tap-bugsnag";
  arguments = {
    envSrc = src;
  };
  searchPaths = {
    envPaths = [
      formatter
    ];
    envSources = [
      generic.linter
      env.tap-bugsnag.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/builders/lint_and_format.sh";
}
