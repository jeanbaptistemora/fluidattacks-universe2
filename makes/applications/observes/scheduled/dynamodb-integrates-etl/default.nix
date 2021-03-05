{ observesPkgs
, makeEntrypoint
, path
, ...
}:
let
  computeOnAws = import (path "/makes/utils/compute-on-aws") path observesPkgs;
  jobConfig = {
    attempts = 5;
    command = [ "./m" "observes.job.dynamodb-table-etl" ];
    jobname = "dynamodb-etl";
    jobqueue = "spot_soon";
    name = "aws-batch-dynamodb-etl";
    product = "observes";
    secrets = [
      "OBSERVES_PROD_AWS_ACCESS_KEY_ID"
      "OBSERVES_PROD_AWS_SECRET_ACCESS_KEY"
    ];
    timeout = 7200;
    vcpus = 1;
  };
  dynamoEtlOnAws = computeOnAws jobConfig;
in
makeEntrypoint {
  searchPaths = {
    envPaths = [
      dynamoEtlOnAws
      observesPkgs.coreutils
      observesPkgs.jq
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-dynamodb-integrates-etl";
  template = path "/makes/applications/observes/scheduled/dynamodb-integrates-etl/entrypoint.sh";
}
