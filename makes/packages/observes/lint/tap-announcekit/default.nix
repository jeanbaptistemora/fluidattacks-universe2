{ makeDerivation
, path
, packages
, ...
}:
with packages.observes;
makeDerivation {
  name = "observes-lint-tap-announcekit";
  arguments = {
    envSrc = path "/observes/singer/tap_announcekit";
  };
  searchPaths = {
    envSources = [
      generic.linter
      env.tap-announcekit.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
