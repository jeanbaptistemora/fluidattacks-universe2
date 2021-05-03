{ makeDerivation
, path
, packages
, ...
}:
with packages.observes;
makeDerivation {
  name = "observes-lint-paginator";
  arguments = {
    envSrc = path "/observes/common/paginator";
  };
  searchPaths = {
    envSources = [
      generic.linter
      env.paginator.development
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
