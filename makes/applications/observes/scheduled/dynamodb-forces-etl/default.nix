{ observesPkgs
, path
, ...
}:
let
  computeOnAws = import (path "/makes/utils/compute-on-aws") path observesPkgs;
in
computeOnAws {
  attempts = 10;
  command = [ "./m" "observes.job.dynamodb-forces-etl" ];
  jobname = "dynamodb-forces-etl";
  jobqueue = "spot_later";
  name = "aws-batch-dynamodb-forces-etl";
  product = "observes";
  secrets = [
    "OBSERVES_PROD_AWS_ACCESS_KEY_ID"
    "OBSERVES_PROD_AWS_SECRET_ACCESS_KEY"
  ];
  timeout = 18000;
  vcpus = 2;
}
