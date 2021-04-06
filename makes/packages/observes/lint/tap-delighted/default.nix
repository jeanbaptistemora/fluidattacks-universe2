{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-tap-delighted";
  arguments = {
    envSrc = path "/observes/singer/tap_delighted";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.tap-delighted.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
