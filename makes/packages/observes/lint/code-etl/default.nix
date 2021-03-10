{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-code-etl";
  arguments = {
    envSrc = path "/observes/code_etl";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.development.code-etl
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
