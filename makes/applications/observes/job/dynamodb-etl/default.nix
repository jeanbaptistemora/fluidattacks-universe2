{ makeEntrypoint
, observesPkgs
, packages
, path
, ...
} @ _:
let
  nixPkgs = observesPkgs;
in
makeEntrypoint nixPkgs {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages.observes.streamer-dynamodb
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
