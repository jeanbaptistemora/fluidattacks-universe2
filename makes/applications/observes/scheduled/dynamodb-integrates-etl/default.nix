{ computeOnAws
, nixpkgs
, makeEntrypoint
, path
, ...
}:
let
  dynamoEtlOnAws = computeOnAws {
    attempts = 5;
    command = [ "./m" "observes.job.dynamodb-table-etl" ];
    jobname = "dynamodb-etl";
    jobqueue = "spot_soon";
    name = "aws-batch-dynamodb-etl";
    product = "observes";
    secrets = [
      "GITLAB_API_TOKEN"
    ];
    timeout = 7200;
    vcpus = 1;
  };
in
makeEntrypoint {
  searchPaths = {
    envPaths = [
      dynamoEtlOnAws
      nixpkgs.coreutils
      nixpkgs.jq
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-dynamodb-integrates-etl";
  template = path "/makes/applications/observes/scheduled/dynamodb-integrates-etl/entrypoint.sh";
}
