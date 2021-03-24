{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-paginator";
  arguments = {
    envSrc = path "/observes/common/paginator";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.development.paginator
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
