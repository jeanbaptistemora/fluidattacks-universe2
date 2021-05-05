{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-service-jobs-scheduler";
  arguments = {
    envSrc = path "/observes/services/jobs_scheduler";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.service-jobs-scheduler.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
