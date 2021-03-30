{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-tap-csv";
  arguments = {
    envSrc = path "/observes/singer/tap_csv";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.tap-csv.development
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
