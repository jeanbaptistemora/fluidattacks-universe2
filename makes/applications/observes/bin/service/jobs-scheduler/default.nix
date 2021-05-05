{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from jobs_scheduler import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.service-jobs-scheduler.runtime
    ];
  };
  name = "observes-bin-service-jobs-scheduler";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}
