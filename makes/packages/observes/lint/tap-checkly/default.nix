{ makeDerivation
, path
, packages
, ...
}:
with packages.observes;
makeDerivation {
  name = "observes-lint-tap-checkly";
  arguments = {
    envSrc = path "/observes/singer/tap_checkly";
  };
  searchPaths = {
    envSources = [
      generic.linter
      env.tap-checkly.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
