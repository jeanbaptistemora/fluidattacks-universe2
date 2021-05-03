{ makeDerivation
, path
, packages
, ...
}:
with packages.observes;
makeDerivation {
  name = "observes-lint-tap-delighted";
  arguments = {
    envSrc = path "/observes/singer/tap_delighted";
  };
  searchPaths = {
    envSources = [
      generic.linter
      env.tap-delighted.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
