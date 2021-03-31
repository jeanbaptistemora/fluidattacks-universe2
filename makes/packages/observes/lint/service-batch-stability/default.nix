{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-service-batch-stability";
  arguments = {
    envSrc = path "/observes/services/batch_stability";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.service-batch-stability.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
