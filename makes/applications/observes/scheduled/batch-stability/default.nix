{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.service.batch-stability
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  name = "observes-scheduled-batch-stability";
  template = path "/makes/applications/observes/scheduled/batch-stability/entrypoint.sh";
}
