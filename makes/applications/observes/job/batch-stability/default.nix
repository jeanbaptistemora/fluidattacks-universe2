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
  name = "observes-job-batch-stability";
  template = path "/makes/applications/observes/job/batch-stability/entrypoint.sh";
}
