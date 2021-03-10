{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-dif-gitlab-etl";
  arguments = {
    envSrc = path "/observes/etl/dif_gitlab_etl";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.development.dif-gitlab-etl
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
