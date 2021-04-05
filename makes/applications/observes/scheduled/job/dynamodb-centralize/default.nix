{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages.observes.bin.service.migrate-tables
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-dynamodb-centralize";
  template = path "/makes/applications/observes/scheduled/job/dynamodb-centralize/entrypoint.sh";
}
