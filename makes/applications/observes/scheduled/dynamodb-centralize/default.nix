{ observesPkgs
, path
, ...
}:
let
  computeOnAws = import (path "/makes/utils/compute-on-aws") path observesPkgs;
in
computeOnAws {
  attempts = 5;
  command = [ "./m" "observes.job.dynamodb-centralize" ];
  jobname = "dynamodb-centralize";
  jobqueue = "spot_soon";
  name = "observes-scheduled-dynamodb-centralize";
  product = "observes";
  secrets = [
    "OBSERVES_PROD_AWS_ACCESS_KEY_ID"
    "OBSERVES_PROD_AWS_SECRET_ACCESS_KEY"
  ];
  timeout = 1800;
  vcpus = 1;
}
