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
      packages.observes.streamer-dynamodb
      packages.observes.tap-json
      packages.observes.target-redshift
      packages.observes.update-sync-date
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-job-dynamodb-etl";
  template = path "/makes/applications/observes/job/dynamodb-etl/entrypoint.sh";
}
