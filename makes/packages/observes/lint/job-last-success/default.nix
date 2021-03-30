{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-job-last-success";
  arguments = {
    envSrc = path "/observes/services/update_s3_last_sync_date";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.linter
      packages.observes.env.job-last-success.runtime
    ];
  };
  builder = path "/makes/packages/observes/generic/linter/lint_builder.sh";
}
