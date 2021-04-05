{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages.observes.bin.service.job-last-success
      packages.observes.bin.streamer-dynamodb
      packages.observes.tap-json
      packages.observes.target-redshift
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-job-dynamodb-etl";
  template = path "/makes/applications/observes/job/dynamodb-etl/entrypoint.sh";
}
