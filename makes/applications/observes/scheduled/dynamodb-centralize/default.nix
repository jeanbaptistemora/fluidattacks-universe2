{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages.observes.service.migrate-tables
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-dynamodb-centralize";
  template = path "/makes/applications/observes/scheduled/dynamodb-centralize/entrypoint.sh";
}
