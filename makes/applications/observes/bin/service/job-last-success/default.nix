{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from job_last_success.cli import main";
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
