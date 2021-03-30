{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-singer-io";
  arguments = {
    envSrc = path "/observes/common/singer_io";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.development.singer-io
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
