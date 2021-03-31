{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.service.batch-stability
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  name = "observes-scheduled-job-batch-stability";
  template = path "/makes/applications/observes/scheduled/job/batch-stability/entrypoint.sh";
}
