{ makeEntrypoint
, packages
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.service.jobs-scheduler
    ];
  };
  name = "observes-scheduled-job-scheduler";
  template = "observes-bin-service-jobs-scheduler";
}
