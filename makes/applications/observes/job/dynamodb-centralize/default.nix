{ makeEntrypoint
, observesPkgs
, packages
, path
, ...
}:
makeEntrypoint observesPkgs {
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
  name = "observes-job-dynamodb-centralize";
  template = path "/makes/applications/observes/job/dynamodb-centralize/entrypoint.sh";
}
