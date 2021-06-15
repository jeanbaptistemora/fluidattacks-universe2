{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-tap-gitlab";
  arguments = {
    envSrc = path "/observes/singer/tap_gitlab";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.tap-gitlab.development
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
