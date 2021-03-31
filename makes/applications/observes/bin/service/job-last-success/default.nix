{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from update_s3_last_sync_date.cli import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.job-last-success.runtime
    ];
  };
  name = "observes-bin-service-job-last-success";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
