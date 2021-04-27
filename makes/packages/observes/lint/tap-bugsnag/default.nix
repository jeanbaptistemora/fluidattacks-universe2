{ makeDerivation
, path
, packages
, ...
}:
with packages.observes;
makeDerivation {
  name = "observes-lint-tap-bugsnag";
  arguments = {
    envSrc = path "/observes/singer/tap_bugsnag";
  };
  searchPaths = {
    envSources = [
      generic.linter
      env.tap-bugsnag.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
