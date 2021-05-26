{ makeDerivation
, path
, packages
, ...
}:
with packages.observes;
makeDerivation {
  name = "observes-lint-tap-json";
  arguments = {
    envSrc = path "/observes/singer/tap_json";
  };
  searchPaths = {
    envSources = [
      generic.linter
      env.tap-json.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
