{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-tap-mixpanel";
  arguments = {
    envSrc = path "/observes/singer/tap_mixpanel";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.tap-mixpanel.development
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
