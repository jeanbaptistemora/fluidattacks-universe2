{ makeDerivation
, path
, packages
, ...
}:
with packages.observes;
makeDerivation {
  name = "observes-lint-singer-io";
  arguments = {
    envSrc = path "/observes/common/singer_io";
  };
  searchPaths = {
    envSources = [
      generic.linter
      env.singer-io.development
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
